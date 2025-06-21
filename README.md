# free-on-pypi

## Opis
Narzędzie do sprawdzania dostępności nazw pakietów na PyPI. Dostarcza dwa tryby pracy:

1. Tryb pliku - sprawdza listę nazw z pliku tekstowego
2. Tryb generatora - sprawdza wszystkie kombinacje "aba" (gdzie a i b to małe litery alfabetu)

## Instalacja

```bash
pip install requests
```

## Użycie

### Tryb pliku (from_file)
Sprawdza dostępność nazw z pliku tekstowego:

```bash
python pypi.py from_file
python github.py from_file
```

Domyślne parametry:
- Plik wejściowy: `names.txt`
- Plik wynikowy z nazwami wolnymi: `free.txt`
- Plik wynikowy z nazwami zajętymi: `busy.txt`
- Opóźnienie między zapytaniami: 100ms

Można zmienić parametry podając je jako argumenty:
```python
from_file(INPUT_FILE="custom_names.txt", FREE_FILE="custom_free.txt", BUSY_FILE="custom_busy.txt", DELAY=0.2)
```

### Tryb generatora (generator)
Automatycznie sprawdza wszystkie kombinacje "aba" (np. "aba", "aca", "ada" itp.):

```bash
python pypi.py generator
python github.py generator
```

Domyślne parametry:
- Plik wynikowy z nazwami wolnymi: `free.txt`
- Plik wynikowy z nazwami zajętymi: `busy.txt`
- Plik postępu: `progress.txt`
- Opóźnienie między zapytaniami: 100ms

Można zmienić parametry podając je jako argumenty:
```python
generator(FREE_FILE="custom_free.txt", BUSY_FILE="custom_busy.txt", PROGRESS_FILE="custom_progress.txt", DELAY=0.2)
```

## Funkcje

### from_file(INPUT_FILE="names.txt", FREE_FILE="free.txt", BUSY_FILE="busy.txt", DELAY=0.1)
- Sprawdza dostępność nazw z pliku tekstowego
- Zapisuje wyniki do plików wyjściowych
- Domyślnie używa opóźnienia 100ms

### generator(FREE_FILE="free.txt", BUSY_FILE="busy.txt", PROGRESS_FILE="progress.txt", DELAY=0.1)
- Generuje i sprawdza wszystkie kombinacje "aba"
- Zapisuje postęp do pliku
- Możliwe wznowienie z poprzedniego miejsca
- Domyślnie używa opóźnienia 100ms

## Wyjście
- Nazwy wolne: zapisywane do pliku `free.txt`
- Nazwy zajęte: zapisywane do pliku `busy.txt`
- Postęp (tylko dla generatora): zapisywany do pliku `progress.txt`

## Uwagi
- Narzędzie używa opóźnienia między zapytaniami, aby uniknąć przeciążenia serwerów PyPI
- Wszystkie nazwy są sprawdzane w formie małych liter
- Pliki wynikowe są zapisywane w trybie append (dodawanie) dla generatora
- Generator może być wznowiony z poprzedniego miejsca dzięki plikowi postępu
