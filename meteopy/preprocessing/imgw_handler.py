from __future__ import annotations

import unicodedata
from pathlib import Path
import time
import numpy as np
import pandas as pd

from meteopy.consts.dirs import Dirs
from meteopy.utils.log_module import get_logger


class IMGWDataHandler:
    def __init__(self):
        self.logger = get_logger("IMGWDataHandler")



    def split_csv_by_station(self, csv_file: Path, output_dir: Path, encoding: str = Dirs.ENCODING):
        """Dzieli plik CSV na osobne pliki według nazwy stacji i roku.

        Args:
            csv_file (Path): Ścieżka do pliku wejściowego.
            output_dir (Path): Katalog, w którym zapisane zostaną pliki wyjściowe.
            encoding (str): Kodowanie pliku wejściowego i wyjściowego.

        """
        try:
            df = pd.read_csv(csv_file, encoding=encoding)
        except Exception as e:
            self.logger.critical(f"Błąd wczytywania {csv_file}: {e}")
            return

        if df.shape[1] < 3:
            self.logger.error(f"Plik {csv_file} ma niepoprawny format (za mało kolumn).")
            return

        df.columns = ["ID", "Station", "Year", "Month", "Day"] + list(df.columns[5:])

        for (id), group in df.groupby("ID"):
            output_file = output_dir / f"{id}.csv"
            file_exists = Path(output_file).exists()

            group.to_csv(output_file, mode="a" if file_exists else "w",
                         encoding=encoding, index=False, header=not file_exists)

            self.logger.info(f"Zapisano tryb: {'dopisywanie' if file_exists else 'nowy plik'}")

    def divide_downloaded(self, encoding=Dirs.ENCODING):
        base_input_dir = Dirs.DATA_DIR
        base_output_dir = Dirs.SEPARATED_DIR

        for subdir in base_input_dir.iterdir():
            if subdir.is_dir():
                output_subdir = base_output_dir / subdir.name
                output_subdir.mkdir(parents=True, exist_ok=True)

                for csv_file in subdir.rglob("*.csv"):
                    self.split_csv_by_station(csv_file, output_subdir, encoding)
                    try:
                        csv_file.unlink()
                    except Exception:
                        self.logger.exception("Błąd podczas usuwania pliku %s", csv_file.name)
                    else:
                        self.logger.info(f"Usunięto plik: {csv_file.name}")
        self.logger.info("Podział plików zakończony.")

    def replace_with_na(self, data_frame: pd.DataFrame, column_indices: list[int]) -> pd.DataFrame:
        """Sprawdza, czy w DataFrame w kolumnie o podanym indeksie (lub liście indeksów) znajduje się wartość "8", a
        następnie zmienia dane w poprzedniej kolumnie w tym wierszu na NaN.

        Args:
            data_frame (pd.DataFrame): DataFrame do przetworzenia.
            column_indices (list[int]): Lista indeksów kolumn do sprawdzenia.

        Returns:
            pd.DataFrame: Zaktualizowany DataFrame.

        """
        for col_index in column_indices:
            if col_index > 0:  # Upewnij się, że nie próbujemy zmienić danych w kolumnie o indeksie -1
                mask = data_frame.iloc[:, col_index] == 8
                data_frame.loc[mask, data_frame.columns[col_index - 1]] = np.nan
        return data_frame

    def fill_missing_data(self, data_frame: pd.DataFrame, value_cols: list[str], mode: int) -> pd.DataFrame:
        """Uzupełnia brakujące dane w DataFrame w zależności od wybranego trybu.

        Args:
            data_frame (pd.DataFrame): DataFrame zawierający dane.
                        value_cols list(str): Nazwy kolumn z wartościami do uzupełnienia.
            mode (int): Tryb uzupełniania brakujących danych:
                1 - zostawia brakujące dane bez zmian.
                2 - uzupełnia brakujące dane wartością z poprzedniego dnia.
                3 - uzupełnia brakujące dane średnią z 50 poprzednich dni.

        Returns:
            pd.DataFrame: DataFrame z uzupełnionymi danymi.

        """
        if mode == 1:
            # Tryb 1: zostawia brakujące dane bez zmian
            return data_frame

        if mode == 2:
            # Tryb 2: uzupełnia brakujące dane wartością z poprzedniego dnia
            for col in value_cols:
                data_frame[col] = data_frame[col].ffill()

        elif mode == 3:
            # Tryb 3: uzupełnia brakujące dane średnią z 50 poprzednich dni
            for col in value_cols:
                self.logger.debug("Checking {}".format(col))
                data_frame.loc[0, col] = 0 if pd.isna(data_frame.loc[0, col]) else data_frame.loc[0, col]
                start_time = time.time()
                while data_frame[col].isna().sum() > 0:
                    if time.time() - start_time >=1:
                        self.logger.warning("problem z obliczeniem śrdniej, stosowanie 2 trybu")
                        return self.fill_missing_data(data_frame, value_cols, 2)
                    else:
                        data_frame[col] = data_frame[col].fillna(data_frame[col].rolling(window=50, min_periods=1).mean())
        else:
            self.logger.critical("Nieprawidłowy tryb. Wybierz 1, 2 lub 3.")
        return data_frame
    
    def merge_to_date(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Łączy kolumny z datą w jedną kolumnę. UWAGA: kolumny z datą muszą być nazwane 'Year', 'Month' i 'Day'.

        Args:
            data_frame (pd.DataFrame): DataFrame zawierający dane.

        Returns:
            pd.DataFrame: DataFrame z połączoną kolumną z datą.

        """
        data_frame["Data"] = pd.to_datetime(data_frame[['Year', 'Month', 'Day']].rename(columns={"Year": "year", "Month": "month", "Day": "day"}))
        cols = list(data_frame.columns)
        cols.insert(2, cols.pop(cols.index("Data")))
        data_frame=data_frame[cols]
        data_frame = data_frame.drop(columns=['Year', 'Month', 'Day'])

        return data_frame

    def preprocess(self, mode: int) -> None:
        """Przetwarza dane meteorologiczne.

        Args:
        mode (int): Tryb uzupełniania brakujących danych:
            1 - zostawia brakujące dane bez zmian.
            2 - uzupełnia brakujące dane wartością z poprzedniego dnia.
            3 - uzupełnia brakujące dane średnią z 50 poprzednich dni.

        """
        Directory = Dirs.SEPARATED_DIR / "klimat"
        if Directory.exists():
            self.logger.info(f"Preprocessowanie {Path(Directory).name}")
            for csv_file in Directory.glob("*.csv"):
                df = pd.read_csv(csv_file, encoding=Dirs.ENCODING, dtype={15: str})
                if df.shape[1] ==9:
                    self.logger.warning(f"plik {csv_file} został już przeprocesowany lub jest uszkodzony")
                    continue
                elif df.shape[1] != 18:
                    self.logger.critical(f"plik {csv_file} uszkodzony -> usuwanie")
                    csv_file.unlink()
                    continue
                df = self.replace_with_na( df, [6,8,10,12,14,17])
                df[['Year', 'Month', 'Day']] = df[['Year', 'Month', 'Day']].apply(pd.to_numeric, errors='coerce')
                df.dropna(subset=['Year', 'Month', 'Day'], inplace=True)
                df.drop(columns=df.columns[[6,8,10,12,14,15,17]], inplace=True)
                self.logger.debug("Usunięto kolumny z niepotrzebnymi danymi")
                df.columns=["Kod_stacji", "Nazwa_stacji", "Year", "Month", "Day", "Maksymalna_temperatura_dobowa_[C]", "Minimalna_temperatura_dobowa_[C]", "Srednia_temperatura_dobowa_[C]", "Temperatura_minimalna_przy_gruncie_[C]", "Suma_dobowa_opadow_[mm]", "Wysokosc_pokrywy_snieznej_[cm]"]
                df.sort_values( ['Year', 'Month', 'Day'], ascending=[True, True, True], inplace=True )

                self.logger.debug("Filling missing data")
                df = self.fill_missing_data(df, df.columns[[6,7,8]], mode)
                df[df.columns[[9,10]]] = df[df.columns[[9,10]]].fillna(0)
                self.logger.debug("Zmiana daty")
                df=self.merge_to_date(df)
                df.to_csv(csv_file, encoding=Dirs.ENCODING, index=False)
                
            self.logger.info(f"pomyślnie przetworzono katalog: {Directory}")


        Directory = Dirs.SEPARATED_DIR / "opad"
        if Directory.exists():
            self.logger.info(f"Preprocessowanie {Path(Directory).name}")
            for csv_file in Directory.glob("*.csv"):
                df = pd.read_csv(csv_file, encoding=Dirs.ENCODING, dtype={15: str})
                if df.shape[1] == 6:
                    self.logger.warning(f"plik {csv_file} został już przeprocesowany lub jest uszkodzony")
                    continue
                if df.shape[1] != 16:
                    self.logger.critical(f"plik {csv_file} uszkodzony -> usuwanie")
                    csv_file.unlink()
                    continue
                df = self.replace_with_na(df, [6, 9, 11])
                df[["Year", "Month", "Day"]] = df[["Year", "Month", "Day"]].apply(pd.to_numeric, errors="coerce")
                df.dropna(subset=["Year", "Month", "Day"], inplace=True)
                df.drop(columns=df.columns[[6, 7, 9, 11, 12, 13, 14, 15]], inplace=True)
                df.columns = ["Kod_stacji", "Nazwa_stacji", "Year", "Month", "Day", "Suma_dobowa_opadow_[mm]", "Wysokosc_pokrywy_sniesnej_[cm]", "Wysokosc_swiezospalego_sniegu_[cm]"]
                df.sort_values(["Year", "Month", "Day"], ascending=[True, True, True], inplace=True)
                self.logger.debug(f"Filling missing data {csv_file}")
                df = self.fill_missing_data(df, df.columns[[5]], mode)      # uzupełnia dane wydług trybu
                df[df.columns[[6, 7]]] = df[df.columns[[6, 7]]].fillna(0)       # uzupełnia dane n/a zerami tam gdzie średnie są bezsensu
                self.logger.debug("merging: {csv_file}")
                df = self.merge_to_date(df)
                df.to_csv(csv_file, encoding=Dirs.ENCODING, index=False)
            self.logger.info(f"pomyślnie przetworzono katalog: {Directory}")

        Directory = Dirs.SEPARATED_DIR / "synop"
        if Directory.exists():
            self.logger.info(f"Preprocessowanie {Path(Directory).name}")
            for csv_file in Directory.glob("*.csv"):
                df = pd.read_csv(csv_file, encoding=Dirs.ENCODING, dtype={15: str})
                if df.shape[1] == 12:
                    self.logger.warning(f"plik {csv_file} został już przeprocesowany lub jest uszkodzony")
                    continue
                if df.shape[1] != 23:
                    self.logger.critical(f"plik {csv_file} uszkodzony -> usuwanie")
                    csv_file.unlink()
                    continue
                df = self.replace_with_na(df, [6, 8, 10, 12, 14, 16, 18, 20, 22])
                df[["Year", "Month", "Day"]] = df[["Year", "Month", "Day"]].apply(pd.to_numeric, errors="coerce")
                df.dropna(subset=["Year", "Month", "Day"], inplace=True)
                df.drop(columns=df.columns[[6, 8, 10, 12, 14, 16, 18, 20, 22]], inplace=True)
                df.columns = ["Kod_stacji", "Nazwa_stacji", "Year", "Month", "Day", "Zachmurzenie_[oktany]", "Srednia_dobowa_predkosc_wiatru_[m/s]", "Srednia_temperatura_dobowa_[C]", "Srednia_dobowe_cisnienie_pary_wodnej_[hPa]", "Srednia_dobowa_wilgotnosc_wzgledna_[%]", "Srednia_dobowe_cisnienie_na_poziomie_stacji_[hPa]", "Srednie_dobowe_cisnienie_na_pozimie_morza_[hPa]", "Suma_opadu_dzien_[mm]", "Suma_opadu_noc_[mm]"]

                df.sort_values(["Year", "Month", "Day"], ascending=[True, True, True], inplace=True)
                df = self.fill_missing_data(df, df.columns[[5, 6, 7, 8, 9, 10, 11]], mode)
                df[df.columns[[12, 13]]] = df[df.columns[[12, 13]]].fillna(0)
                df = self.merge_to_date(df)
                df.to_csv(csv_file, encoding=Dirs.ENCODING, index=False)
                self.logger.debug(f"pomyślnie preprocessowano plik: {Path(csv_file).name}")
            self.logger.info(f"pomyślnie przetworzono katalog: {Directory}")
