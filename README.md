# Analiza danych meteorologicznych

## Instrukcja uruchomienia

1. **Klonowanie repozytorium**

    ```bash
    git clone https://github.com/TwojeRepozytorium/python-1-project-AntoniTrzebuniak.git
    cd python-1-project-AntoniTrzebuniak
    ```

2. **Zainstalowanie pakietu**
    uruchomić z folderu repozytorium komendę

```bash
pip install -e .
```

## Opis funkcjonalności

Po zainstalowaniu pakietu można z niego kożystać wpisując poniższe komendy w terminalu, można też wpisać meteopy --help żeby zobaczyć komendy w każdej chwili

- **Pobieranie danych**:

```bash
meteopy download
```

Komenda przeprowadza użytkownika przez process pobierania i preprocessingu danych krok po kroku.
Możliwe jest pobranie danych tylko jednego typu na raz, można ją wywołać kilkukrotnie
Użytkownik jest pytany o typ danych do pobrania, zakres lat z ktyh dane mają być pobrane i sposób radzenia sobie z brakującymi danymi

- **Pełna analiza**:

```bash
meteopy full_analysis
```

Komenda przeprowadza cały process pobierania, preprocessingu i korzysta z wszystkich funkcjonalności (tworzy wykres liniowy, histogram, wykres korelacji, plik tekstowy z statystykami oraz wykres z modelem przewidywania regresją liniową) dla wszystkich stacji dla wszystkich dostępnych parametrów dla pobranego typu danych

- **Podstawowe Statystyki**:

```bash
meteopy basic_summary <data_type>
```

Komenda przyjmuje argument typu int, który wybiera typ danych: 1-klimat, 2-opad, 3-synop. Następnie interaktywnie przeprowadza użytkownika przez wybór reszty argumentów.
Komenda wybiera 5 losowych stacji, dla każdego parametru wybranego przez użytkownika: generuje podstawowe statystyki, zapisuje do pliku, generuje 3 rodzaje wykresów \[boxplot, histogram, liniowy\], zapisuje je do pliku.

-**Czyszczenie danych**

```bash
meteopy drop_data
```

Usuwa katalog z przetworzonymi danymi, zalecam stosować przed pobraniem danych tego samego typu ponownie, unikna się w ten sposób błędów związanych z dopisywaniem nie przetworzonych danych do przetworzonych.

### wybrane elementy

- **Radzenie sobie z niestandardową reprezentacją brakujących danych**:
    W preprocessingu sprawdzane są statusy pomiarów i jeśli status=8, czyli brak pomiaru wartość w poprzedniej kolumnie jest zmieniana na NaN, domyślnie jest to 0, co wprowadza problem, bo nie da się tego odróżnić od poprawnej wartości
    Następnie kolumny z statusami są usuwane gdyż nie będą potrzebne w analizie danych.

- **Sposoby uzupełniania brakujących danych**:
    Użytkownik ma do wyboru sposób uzupełnienia brakujących danych
    1 - zostawia brakujące dane bez zmian. (wartości NaN będą pomijane przy tworzeniu wykresu)
    2 - uzupełnia brakujące dane wartością z poprzedniego dnia.
    3 - uzupełnia brakujące dane średnią z 50 poprzednich dni.

- **Funkcje do wizualizacji danych**:
    Funkcje do wizualizacji danych mogą tworzyć wykresy/statystyki dla wielu stacji i wielu parametrów, jeśli stację albo parametry są nie podane to biorą wszystkie dostępne. użytkownik może również wybierać zakres dat w jakich chce żeby wykres powstał, jedyną wada jest to, że nie może wywołać samych funkcji z cli, funkcjonalność zostanie dodana w przyszłych wersjach

- **Pobieranie danych**
    Z powodu innej stuktury katalogów w synop na stronie internetowej, została stworzona klasa bazowa fetchera i dwie podklasy, które miały inne implementacje funkcji fetch. Miało to ułatwić organizację kodu i kożystanie, ale jako że była to tylko jedna różniąca się funkcja, bo inne były w innych modułach lepiej było to zrobić na ifie.
