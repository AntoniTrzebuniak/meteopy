## Założenia

W ramach projektu ma powstać **narzędzie analityczne** dla [danych meteorologicznych zgromadzonych w danych otwartych Instytutu Meteorologii i Gospodarki Wodnej](https://danepubliczne.imgw.pl/). Ma ono służyć do zautomatyzowanego pobierania, analizy i prezentacji danych.

## Kod startowy

Kod startowy do rozpoczęcia projektu znajduje się w [repozytorium](https://github.com/agh-geoinf/python-1-project).

## Opis zadań i struktury tworzonego pakietu

### Etap 0 - przygotowanie

Stwórz repozytorium.

Stwórz subpakiet `utils`, w którym dodasz moduł `logging` wraz z zaimplementowaną funkcją `get_logger` do konfiguracji logowania.

Stwórz subpakiet `consts`, który będzie służył do przechowywania modułów ze stałymi zmiennymi. Przyjęło się, że zmienne stałe zapisywane są z użyciem dużych liter (np. `ROOT_URL = "https://danepubliczne.imgw.pl"`).

* W tym subpakiecie stwórz moduł `dirs`, gdzie przechowywane będą informacje o lokalnych ścieżkach w projekcie. Użyj tam klasy `Path` z biblioteki `pathlib`.

### Etap 1 - pobieranie danych

W ramach subpakietu o nazwie `data_fetchers` należy przygotować klasę służącą do pobierania danych.

W module `imgw_fetcher` stwórz klasę `IMGWDataFetcher`, która posiadać będzie następujące metody:

* `fetch` - do przeszukiwania katalogów w oparciu o dostępną strukturę - dodaj odpowiednie argumenty,
* `download_file` - do pobrania pliku pod wskazanym URL - pliki mają się pobierać do podkatalogu `./data/downloaded`; metoda musi mieć argument `unzip` typu `bool`, który będzie definiował czy plik ma być wypakowany,

Do klasy należy napisać odpowiednie testy dla wszystkich jej funkcjonalności.

### Etap 2 - preprocessing

W ramach subpakietu o nazwie `preprocessing`, w module `imgw_handler` stwórz klasę `IMGWDataHandler`, która będzie służyć do:

* Modyfikacji formy przechowywania danych - napisz metodą `divide_downloaded`, która przetworzy pobrane dane i zapisze je do osobnych plików w podkatalogu `./data/separated`. Jako propozycja tego podziału, każda stacja ma mieć swój plik, w którym będą przechowywane wszystkie jej parametry.
