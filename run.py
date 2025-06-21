import requests
import string
import time
import json
import os




def is_available(pkg):
    try:
        response = requests.get(f'https://pypi.org/pypi/{pkg}/json')
        return response.status_code == 404
    except requests.RequestException:
        return True  # Assume free if we can't reach PyPI
    except Exception:
        return False


def check_names_from_file(input_file_path="names.txt",
                          delay=0.1,
                          free_file_path="free.txt",
                          busy_file_path="busy.txt"):
    try:
        with open(input_file_path, "r") as infile:
            names = [line.strip().lower() for line in infile if line.strip()]
    except FileNotFoundError:
        print(f"❌ Błąd: Plik '{input_file_path}' nie został znaleziony.")
        return

    print(f"✅ Załadowano {len(names)} nazw z pliku '{input_file_path}'.")

    with open(free_file_path, "w") as free_file, open(busy_file_path, "w") as busy_file:
        for name in names:
            print(f"Sprawdzam: {name}", end="")
            time.sleep(delay)

            if is_available(name):
                print(" ✅ free")
                free_file.write(name + "\n")
                free_file.flush()
                os.fsync(free_file.fileno())
            else:
                print(" ❌ taken")
                busy_file.write(name + "\n")
                busy_file.flush()
                os.fsync(busy_file.fileno())

    print(f"\nZakończono. Wyniki zapisano do:\n- {free_file_path}\n- {busy_file_path}")



def main():
    letters = string.ascii_lowercase
    
    # Check where to resume
    try:
        with open("progress.txt", "r") as f:
            last_checked = f.read().strip()
        start_index = letters.index(last_checked[0])
        print(f"Resuming from: {last_checked}")
    except:
        start_index = 0
        print("Starting from the beginning")
    
    # Open files in append mode
    with open("free.txt", "a") as free_file, open("busy.txt", "a") as busy_file:
        # Continue from the last place
        for i in range(start_index, len(letters)):
            a = letters[i]
            for b in letters:
                name = a + b + a
                
                # Save progress
                with open("progress.txt", "w") as f:
                    f.write(name)
                    f.flush()  # Ensure progress is saved immediately
                
                # Display progress
                total = len(letters) * len(letters)
                current = (i * len(letters)) + letters.index(b) + 1
                progress = (current / total) * 100
                print(f"\rChecking {name} ({current}/{total} - {progress:.1f}%)", end="")
                
                time.sleep(0.1)  # 100 ms delay
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
        os.remove("progress.txt")
    except:
        pass

if __name__ == "__main__":
    # main()
    check_names_from_file()
