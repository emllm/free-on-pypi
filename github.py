import time
import os
import requests
import re

# Czas opóźnienia między zapytaniami (w sekundach)
DELAY = 0.5  # 500 ms

# Lista zarezerwowanych słów PyPI
RESERVED_WORDS = {
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

def is_valid_pypi_name(name):
    """Sprawdza czy nazwa jest dozwolona na PyPI"""
    # Sprawdź czy nazwa jest zarezerwowana
    if name.lower() in RESERVED_WORDS:
        return False
    
    # Sprawdź długość
    if len(name) < 2 or len(name) > 200:
        return False
    
    # Sprawdź znaki
    if not re.match(r'^[a-z0-9_\-]+$', name):
        return False
    
    # Sprawdź czy nie zaczyna się od znaku podkreślenia
    if name.startswith('_'):
        return False
    
    return True

def is_github_username_available(name):
    url = f"https://api.github.com/users/{name}"
    response = requests.get(url)
    return response.status_code == 404

def is_github_org_available(name):
    url = f"https://api.github.com/orgs/{name}"
    response = requests.get(url)
    return response.status_code == 404

def check_names_from_file(input_file="names.txt",
                          free_file="free.txt",
                          busy_file="busy.txt"):
    try:
        with open(input_file, "r") as f:
            names = [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Błąd: Plik '{input_file}' nie istnieje.")
        return

    print(f"✅ Załadowano {len(names)} nazw z pliku '{input_file}'.")
    print("⏳ Sprawdzam dostępność na GitHub...")

    with open(free_file, "w") as f_free, open(busy_file, "w") as f_busy:
        for name in names:
            print(f"🔍 Sprawdzam: {name}", end="")
            time.sleep(DELAY)

            # Sprawdź czy nazwa jest dozwolona na PyPI
            if not is_valid_pypi_name(name):
                print(" ❌ Nieprawidłowa nazwa")
                f_busy.write(f"{name} (nieprawidłowa nazwa)\n")
                f_busy.flush()
                os.fsync(f_busy.fileno())
                continue

            username_free = is_github_username_available(name)
            org_free = is_github_org_available(name)

            if username_free and org_free:
                print(" ✅ Wolne (użytkownik i organizacja)")
                f_free.write(f"{name}\n")
                f_free.flush()
                os.fsync(f_free.fileno())
            else:
                print(" ❌ Zajęte")
                f_busy.write(f"{name}\n")
                f_busy.flush()
                os.fsync(f_busy.fileno())

    print(f"\n✅ Zakończono. Wyniki zapisano do:")
    print(f"- Dostępne: {free_file}")
    print(f"- Zajęte: {busy_file}")



if __name__ == "__main__":
    # main()
    check_names_from_file()
