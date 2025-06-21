import requests
import string
import time
import json
import os
import re


def is_available(pkg):
    """
    Sprawdza dostępność nazwy na PyPI używając wielu metod.
    """
    try:
        # Metoda 1: Sprawdzenie JSON endpoint
        json_response = requests.get(f'https://pypi.org/pypi/{pkg}/json')
        if json_response.status_code == 404:
            return True
        
        # Metoda 2: Sprawdzenie strony HTML
        html_response = requests.get(f'https://pypi.org/project/{pkg}')
        if html_response.status_code == 404:
            return True
            
        # Metoda 3: Sprawdzenie Simple API
        simple_response = requests.get(f'https://pypi.org/simple/{pkg}')
        if simple_response.status_code == 404:
            return True
            
        # Metoda 4: Sprawdzenie Simple API (z ukośnikiem)
        simple_slash_response = requests.get(f'https://pypi.org/simple/{pkg}/')
        if simple_slash_response.status_code == 404:
            return True
            
        # Jeśli żadna z metod nie dała 404, nazwa jest zajęta
        return False
        
    except requests.RequestException as e:
        print(f"⚠️ Błąd podczas sprawdzania {pkg}: {str(e)}")
        # Jeśli nie możemy się połączyć, zakładamy, że nazwa jest wolna
        return True
    except Exception as e:
        print(f"⚠️ Nieoczekiwany błąd podczas sprawdzania {pkg}: {str(e)}")
        return False


def validate_name(name):
    """
    Waliduje nazwę na podstawie zasad PyPI.
    """
    # Nazwa musi mieć co najmniej 2 znaki
    if len(name) < 2:
        return False, "Nazwa musi mieć co najmniej 2 znaki"
        
    # Nazwa nie może zawierać spacji
    if ' ' in name:
        return False, "Nazwa nie może zawierać spacji"
        
    # Nazwa może zawierać tylko małe litery, cyfry, podkreślenia i myślniki
    if not re.match(r'^[a-z0-9_\-]+$', name):
        return False, "Nazwa może zawierać tylko małe litery, cyfry, podkreślenia i myślniki"
        
    # Nazwa nie może zaczynać się od podkreślenia
    if name.startswith('_'):
        return False, "Nazwa nie może zaczynać się od podkreślenia"
        
    # Lista zarezerwowanych słów
    reserved_words = {
        'host', 'python', 'py', 'pip', 'conda', 'anaconda',
        'pypi', 'github', 'git', 'npm', 'node', 'javascript',
        'java', 'ruby', 'rust', 'go', 'c', 'cpp', 'c++',
        'typescript', 'php', 'sql', 'nosql', 'mongodb', 'mysql',
        'postgresql', 'oracle', 'microsoft', 'google', 'amazon',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'k8s',
        'terraform', 'ansible', 'jenkins', 'circleci', 'githubactions',
        'gitlabci', 'travisci', 'bitbucket', 'jenkins', 'travisci',
        'circleci', 'githubactions', 'gitlabci', 'bitbucketpipelines',
        'azurepipelines', 'appveyor', 'codeship', 'drone', 'wercker',
        'shippable', 'semaphore', 'buildkite', 'teamcity', 'bamboo',
        'octopus', 'spinnaker', 'argocd', 'helm', 'kustomize',
        'docker', 'containerd', 'podman', 'crio', 'runc', 'containerd-shim',
        'katacontainers', 'gvisor', 'firecracker', 'crosvm', 'cloud-hypervisor'
    }
    
    # Nazwa nie może być zarezerwowana
    if name.lower() in reserved_words:
        return False, f"Nazwa '{name}' jest zarezerwowana"
        
    return True, "Nazwa jest poprawna"


def check_names_from_file(input_file_path="names.txt",
                          delay=0.1):
    """
    Generator that yields tuples of (name, is_available) for each name in the input file.
    Uses multiple validation and availability checking methods.
    """
    try:
        with open(input_file_path, "r") as infile:
            names = [line.strip().lower() for line in infile if line.strip()]
    except FileNotFoundError:
        print(f"❌ Błąd: Plik '{input_file_path}' nie został znaleziony.")
        return

    print(f"✅ Załadowano {len(names)} nazw z pliku '{input_file_path}'.")

    for name in names:
        print(f"Sprawdzam: {name}", end="")
        time.sleep(delay)

        # Validate name according to PyPI rules
        is_valid, reason = validate_name(name)
        if not is_valid:
            print(f" ❌ {reason}")
            yield name, False, reason
            continue

        # Check availability using multiple methods
        available = is_available(name)
        status = " ✅ free" if available else " ❌ taken"
        print(status)
        yield name, available, None


def from_file(INPUT_FILE="names.txt",
              FREE_FILE="free.txt",
              BUSY_FILE="busy.txt",
              DELAY=0.1
              ):
    """
    Function that processes names from file using the generator and writes results to files.
    Uses default parameter values from the generator function.
    
    Default filenames:
    - Input: names.txt
    - Free: free.txt
    - Busy: busy.txt
    """
    try:
        with open(FREE_FILE, "w") as free_file, open(BUSY_FILE, "w") as busy_file:
            for name, is_available, reason in check_names_from_file(INPUT_FILE, DELAY):
                if is_available:
                    free_file.write(name + "\n")
                    free_file.flush()
                    os.fsync(free_file.fileno())
                else:
                    if reason:  # If there's a validation reason
                        busy_file.write(f"{name} ({reason})\n")
                    else:
                        busy_file.write(name + "\n")
                    busy_file.flush()
                    os.fsync(busy_file.fileno())

        print(f"\nZakończono. Wyniki zapisano do:\n- {FREE_FILE}\n- {BUSY_FILE}")
    except Exception as e:
        print(f"❌ Wystąpił błąd podczas przetwarzania: {str(e)}")


def generator(FREE_FILE="free.txt",
              BUSY_FILE="busy.txt",
              PROGRESS_FILE="progress.txt",
              DELAY=0.1):
    """
    Generator that checks names in the format "aba" (where a and b are lowercase letters).
    
    Default filenames:
    - Free: free.txt
    - Busy: busy.txt
    - Progress: progress.txt
    """
    letters = string.ascii_lowercase

    # Check where to resume
    try:
        with open(PROGRESS_FILE, "r") as f:
            last_name = f.read().strip()
        start_index = letters.index(last_name[0])
        print(f"Resuming from: {last_name}")
    except:
        start_index = 0
        print("Starting from the beginning")

    # Open files in append mode
    with open(FREE_FILE, "a") as free_file, open(BUSY_FILE, "a") as busy_file:
        # Continue from the last place
        for i in range(start_index, len(letters)):
            a = letters[i]
            for b in letters:
                name = a + b + a

                # Save progress
                with open(PROGRESS_FILE, "w") as f:
                    f.write(name)
                    f.flush()  # Ensure progress is saved immediately

                # Display progress
                total = len(letters) * len(letters)
                current = (i * len(letters)) + letters.index(b) + 1
                progress = (current / total) * 100
                print(f"\rChecking {name} ({current}/{total} - {progress:.1f}%)", end="")

                time.sleep(DELAY)  # Delay based on parameter
                if is_available(name):
                    print(f" ✅ free")
                    free_file.write(name + "\n")
                    free_file.flush()  # Ensure immediate write
                    os.fsync(free_file.fileno())  # Force sync to disk
                else:
                    print(f" ❌ taken")
                    busy_file.write(name + "\n")
                    busy_file.flush()  # Ensure immediate write
                    os.fsync(busy_file.fileno())  # Force sync to disk

    # Remove progress file after completion
    try:
        os.remove(PROGRESS_FILE)
    except:
        pass


if __name__ == "__main__":
    # main()
    from_file()
