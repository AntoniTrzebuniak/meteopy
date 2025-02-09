## Założenia

W ramach projektu ma powstać **narzędzie analityczne** dla [danych meteorologicznych zgromadzonych w danych otwartych Instytutu Meteorologii i Gospodarki Wodnej](https://danepubliczne.imgw.pl/). Ma ono służyć do zautomatyzowanego pobierania, analizy i prezentacji danych.

Dokładniej interesują nas dane znajdujące się pod `Dane historyczne` -> `Dane pomiarowo-obserwacyjne` -> `dane_meteorologiczne` -> `dobowe`. Każdy plik z danymi to po prostu skompresowane pliki csv, które hostowane są na serwerach IMGW, tutaj przykładowy link: `https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/2006/2006_06_k.zip`.

???+ tip "Ogólne wymagania i sposób oceniania"
    Projekt powinien spełniać wszystkie omawiane na zajęciach dobre praktyki. Zaleca się korzystanie z omawianych narzędzi do zapewniania jakości dostarczanego kodu. Projekt powinien zawierać także testy.

    W projekcie oceniane będzie nie tylko dostarczenie wszystkich funkcjonalności, ale także sposób implementacji nieopisanych elementów projektu. W niektórych miejscach elementy projektu nie są w pełni zaplanowane, tam oceniane będzie także zaproponowane samodzielnie podejście.

    Rzeczy wysokopoziomowego projektowania, które ja widzę na ten moment, że wymagają samodzielnego przemyślenia:

    - Argumenty dla funkcji, method itp.,
    - Sposób radzenia sobie z brakami danych i zapewnienie jednolitości w danych,
    - Agregacje, wejściowo operujemy na danych dobowych, za pomocą podawanych argumentów lub zakładając z góry jeden wariant, można zdecydować się na robienie analiz na np. agregacjach miesięcznych,
    - Organizacja folderów i struktury zapisywanych danych i wyników,

    W projekcie dodano "Nieobowiązkowe" elementy, są one dla osób chętnych i zainteresowanych stworzeniem bardziej kompleksowego rozwiązania. Mogą być brain pod uwagę przy ostatecznej ocenie, ale ich brak nie będzie obniżał oceny.

## Kod startowy

Kod startowy do rozpoczęcia projektu znajduje się w [repozytorium](https://github.com/agh-geoinf/python-1-project).

## Opis zadań i struktury tworzonego pakietu

### Etap 0 - przygotowanie

Stwórz repozytorium.

Stwórz subpakiet `utils`, w którym dodasz moduł `logging` wraz z zaimplementowaną funkcją `get_logger` do konfiguracji logowania.

Stwórz subpakiet `consts`, który będzie służył do przechowywania modułów ze stałymi zmiennymi. Przyjęło się, że zmienne stałe zapisywane są z użyciem dużych liter (np. `ROOT_URL = "https://danepubliczne.imgw.pl"`).

- W tym subpakiecie stwórz moduł `dirs`, gdzie przechowywane będą informacje o lokalnych ścieżkach w projekcie. Użyj tam klasy `Path` z biblioteki `pathlib`.

### Etap 1 - pobieranie danych

W ramach subpakietu o nazwie `data_fetchers` należy przygotować klasę służącą do pobierania danych.

W module `imgw_fetcher` stwórz klasę `IMGWDataFetcher`, która posiadać będzie następujące metody:

- `fetch` - do przeszukiwania katalogów w oparciu o dostępną strukturę - dodaj odpowiednie argumenty,
- `download_file` - do pobrania pliku pod wskazanym URL - pliki mają się pobierać do podkatalogu `./data/downloaded`; metoda musi mieć argument `unzip` typu `bool`, który będzie definiował czy plik ma być wypakowany; logika tej metody musi sprawdzać czy dany plik nie został już wcześniej pobrany, jeśli tak, nie ma potrzeby ponownego pobierania.

### Etap 2 - preprocessing

W ramach subpakietu o nazwie `preprocessing`, w module `imgw_handler` stwórz klasę `IMGWDataHandler`, która będzie służyć do:

- Modyfikacji formy przechowywania danych - napisz metodą `divide_downloaded`, która przetworzy pobrane dane i zapisze je do osobnych plików w podkatalogu `./data/separated`. Jako propozycja tego podziału: każda stacja ma mieć swój plik, w którym będą przechowywane wszystkie jej parametry.
    - Przyglądnij się danym, jeśli zauważysz jakieś nieścisłości, w swoim kodzie możesz się ich pozbyć (może to być np. nietypowa dla `pandas` reprezentacja braków danych, wykorzystywanie wartości 0, które oznaczają braki danych lub na odwrót).

??? - info "Nieobowiązkowe"
    Zaproponuj sposób radzenia sobie z brakami w danych, stwórz dodatkową metodę albo argument w obecnej, który pozwoli na wypełnianie braków. Tutaj można użyć np. `fillna()` z `pandas`.

### Etap 3 - eksploracyjna analiza danych (EDA)

W ramach subpakietu o nazwie `eda`, w module `imgw_eda_visualizer` przygotuj klasę `IMGWDataVisualizer`, która będzie odpowiadać za tworzenie wykresów i podsumowań danych meteorologicznych. Stwórz dla niej następujące metody:

- `plot_time_series` - tworzy wykres szeregów czasowych wybranego parametru (np. temperatura, opady) dla wybranych stacji (jako argument, który jest listą) w zadanym przedziale czasowym. Jeśli będzie to pusta lista lub użytkownik nie poda tego argumentu, weź wszystkie stacje.

Wykresy powinny być zapisywane w jakimś folderze.

Porada: Jeśli obawiasz się ilość pamięci w swoim komputerze, możesz określić maksymalną ilość stacji, które mogą być na raz wczytane i przetworzone. Zrób to za pomocą zmiennej stałej np. `MAX_STATIONS` i dodaj logikę w odpowiednich miejscach.

Propozycje: Przy wczytywaniu danych operuj na bibliotece `pandas` i jej `DataFrame`. Do generowania wykresów możesz użyć biblioteki `matplotlib` lub `seaborn`.

??? - info "Nieobowiązkowe"
    Metody:

    - `plot_distribution` - tworzy histogram oraz wykres pudełkowy (boxplot) dla wybranego parametru, prezentując rozkład danych.
    - `plot_missing_data_heatmap` - tworzy mapę ciepła (heatmap), przedstawiającą braki danych w poszczególnych okresach. Możesz użyć `pivot_table` z `pandas` i `sns.heatmap`.

### Etap 4 - analizy statystyczne

W ramach subpakietu o nazwie `statistics`, w module `imgw_statistics`, przygotuj klasę `IMGWStatistics`, która będzie oferować funkcje statystyczne dla danych meteorologicznych. Stwórz następujące metody:

- `calculate_basic_stat` - oblicza podstawowe statystyki: średnia, mediana, odchylenie standardowe, kwartyle itp. dla wybranego parametru. Argument odpowiedzialny za listę stacji niech działa tak jak wyżej. W przypadku większej ilości stacji, albo stwórz stwórz jeden `DataFrame` (zagregowane dane) i to na nim oblicz statystyki albo wygeneruj statystyki dla każdej stacji osobno.
- `calculate_correlation` - oblicza współczynnik korelacji między wybranymi parametrami dla jednej lub wielu stacji.

Statystyki powinny być eksportowane do jakiegoś pliku.

Propozycje: Możesz wykorzystać `pearsonr` z `scipy.stats` lub `corr()` z `pandas`.

??? - info "Nieobowiązkowe"
    Metody:

    - `detect_outliers` - wykrywa wartości odstające w danych z wykorzystaniem metody IQR (Interquartile Range) lub odchylenia standardowego.

### Etap 5 - prognozowanie

W ramach subpakietu `forecasting`, w module `imgw_simple_forecaster` stwórz klasę `IMGWSimpleForecaster`, która będzie wykorzystywać proste modele predykcji. Zaimplementuj następujące metody:

- `linear_regression_forecast` - tworzy prosty model regresji liniowej do przewidywania wartości na podstawie danych historycznych.

Miej na uwadze, że jest to raczej średnia metoda dla szeregów czasowych, w ogóle nie uwzględnia np. sezonowości, ale tutaj bardziej chodzi o pokazanie.

Propozycje: Użyj `LinearRegression` z `scikit-learn`.

??? - info "Nieobowiązkowe"
    Metody:

    - `evaluate_forecast` - oblicza miary jakości prognoz, takie jak RMSE (Root Mean Square Error) i MAE (Mean Absolute Error). Jako argumenty możesz podać po prostu wartości faktyczne i te prognozowane.

    Możesz także zaimplementować jakąś metodę, która będzie prognozować, ale wykorzystując bardziej odpowiednie dla szeregów czasowych metody, np. Holt-Winters (Triple Exponential Smoothing), dostępna jest w pakiecie `statsmodels`.

### Etap X - interfejs

W ramach subpakietu `workflows`, stwórz moduł `entrypoint`, który będzie definiował command line interface. Wykorzystaj bibliotekę `click`. Dodaj następujące komendy, które będą odpowiadać różnym konfiguracjom analiz, które będziemy chcieli wykonywać:

!!! warning  "Argumenty przyjmowane przez poszczególne komendy w CLI zaprojektuj samodzielnie!"

- `full_analysis` - wykonaj całą analizę, wykorzystaj wszystkie funkcjonalności,
- `download` - samo pobieranie danych,
- `basic_summary` - wygeneruj podstawowe statystyki.

Komendy zdefiniuj w osobnych modułach. Pamiętaj o dodaniu CLI do pakietu.

### Etap Y - sprawozdanie / dokumentacja

Stwórz krótkie sprawozdanie / dokumentację w `README.md` projektu lub w GitHub Pages.

Interesują mnie przede wszystkim kroki, które będę musiał podjąć, żeby uruchomić kod od zera. A także krótki opis funkcjonalności, z naciskiem na elementy, które zaprojektowali Państwo sami.

Proszę, żeby nie miało to więcej niż objętość 1 strony A4 (na oko).
