# free-on-pypi

## Opis
Narzędzie do sprawdzania dostępności nazw pakietów na PyPI i GitHub. Dostarcza trzy tryby pracy:

1. Tryb pliku - sprawdza listę nazw z pliku tekstowego
2. Tryb generatora - sprawdza wszystkie kombinacje "aba" (gdzie a i b to małe litery alfabetu)
3. Tryb GitHub - sprawdza dostępność nazw na GitHub (użytkownicy i organizacje)

## Instalacja

```bash
pip install requests
```

## Użycie

### Przykłady użycia

#### 1. Sprawdzanie listy nazw z pliku
```bash
# Sprawdzenie nazw z pliku names.txt na PyPI
python pypi.py from_file

# Sprawdzenie nazw z pliku names.txt na GitHub
python github.py from_file
```

#### 2. Sprawdzanie wszystkich kombinacji "ab"
```bash
# Sprawdzenie wszystkich kombinacji "ab" na PyPI
python pypi.py generator
```

#### 3. Używanie niestandardowych plików
```python
# PyPI z niestandardowymi plikami
from_file(
    INPUT_FILE="my_names.txt",
    FREE_FILE="available_packages.txt",
    BUSY_FILE="taken_packages.txt",
    DELAY=0.2
)

# GitHub z niestandardowymi plikami
from_file(
    INPUT_FILE="usernames.txt",
    FREE_FILE="available_users.txt",
    BUSY_FILE="taken_users.txt",
    DELAY=0.5
)
```

#### 4. Wznowienie przerwanego sprawdzania
```bash
# Generator automatycznie wznowi sprawdzanie od ostatniego miejsca
python pypi.py generator
```

#### 5. Sprawdzanie nazw z walidacją
```python
# Przykład wyniku dla nazwy nieprawidłowej dla PyPI
# Zostanie zapisana do pliku busy.txt jako:
"beta (Nazwa jest zarezerwowana)"

# Przykład wyniku dla nazwy zajętej
# Zostanie zapisana do pliku busy.txt jako:
"numpy"

# Przykład wyniku dla nazwy wolnej
# Zostanie zapisana do pliku free.txt jako:
"mycoolpackage"
```

#### 6. Przykład zawartości pliku names.txt
```
myproject
cooltool
awesomeapp
pythonlib
```

#### 7. Przykład zawartości pliku usernames.txt
```
johnsmith
devopsuser
githubuser
```

#### 8. Opcje zaawansowane
```python
# Zwiększenie opóźnienia dla większej liczby nazw
from_file(INPUT_FILE="big_list.txt", DELAY=0.5)

# Używanie generatora z innym plikiem postępu
generator(PROGRESS_FILE="my_progress.txt", DELAY=0.15)
```

## Funkcje

### PyPI Checking (pypi.py)
- Sprawdza dostępność nazw na PyPI używając wielu metod
- Waliduje nazwy według zasad PyPI
- Zapisuje wyniki do plików wyjściowych
- Domyślnie używa opóźnienia 100ms

### GitHub Checking (github.py)
- Sprawdza dostępność nazw na GitHub (użytkownicy i organizacje)
- Zapisuje wyniki do plików wyjściowych
- Domyślnie używa opóźnienia 500ms

## Walidacja nazw na PyPI
Nazwy na PyPI muszą spełniać następujące warunki:
1. Długość: co najmniej 2 znaki
2. Znaki: małe litery, cyfry, podkreślenia i myślniki
3. Nie może zaczynać się od podkreślenia
4. Nie może zawierać spacji
5. Nie może być zarezerwowana (np. 'python', 'pypi', 'github' itp.)

Lista zarezerwowanych słów:
- host, python, py, pip, conda, anaconda
- pypi, github, git, npm, node, javascript
- java, ruby, rust, go, c, cpp, c++
- typescript, php, sql, nosql, mongodb, mysql
- postgresql, oracle, microsoft, google, amazon
- aws, azure, gcp, docker, kubernetes, k8s
- terraform, ansible, jenkins, circleci, githubactions
- gitlabci, travisci, bitbucket
- i wiele innych...

## Wyjście
- Nazwy wolne: zapisywane do pliku `free.txt`
- Nazwy zajęte: zapisywane do pliku `busy.txt`
- Postęp (tylko dla generatora): zapisywany do pliku `progress.txt`

## Uwagi
- Narzędzie używa opóźnienia między zapytaniami, aby uniknąć przeciążenia serwerów
- Wszystkie nazwy są sprawdzane w formie małych liter
- Pliki wynikowe są zapisywane w trybie append (dodawanie) dla generatora
- Generator może być wznowiony z poprzedniego miejsca dzięki plikowi postępu
- Nazwy nieprawidłowe dla PyPI zostają zapisane w pliku busy.txt z powodem odrzucenia
