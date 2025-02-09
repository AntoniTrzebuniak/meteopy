from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from meteopy.consts.dirs import Dirs
from meteopy.utils.log_module import get_logger


class IMGWDataVisualizer:

    def __init__(self):
        self.data_dir = Dirs.SEPARATED_DIR
        self.output_dir = Dirs.PLOTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger(__name__)
        # Mapowanie typów danych na dostępne parametry
        self.parameter_map = Dirs.PARAMETER_MAP

    def plot_time_series(self, data_type: str, parameters: list[str], start_date: str, end_date: str, stations: list[str] = None) -> None:
        """Tworzy wykres szeregów czasowych dla wybranego parametru i stacji.

        Args:
            data_type (str): Typ danych.
            parameters (list[str], optional): Nazwy parametrów do analizy.
            start_date (str): Początkowa data w formacie 'YYYY-MM-DD'.
            end_date (str): Końcowa data w formacie 'YYYY-MM-DD'.
            stations (list[str]): Lista ID stacji. Jeśli None, wykresy są tworzone dla wszystkich stacji.
        """
        if parameters == []:
            self.logger.info("Analiza dla wszystkich parametrów")
            parameters = self.parameter_map[data_type]

        for parameter in parameters:
            if parameter not in self.parameter_map[data_type]:
                self.logger.error("Parametr '%s' nie jest dostępny dla typu danych '%s'.", parameter, data_type)
                return
            datadir = Path(self.data_dir / data_type)
            available_stations = [d.name for d in datadir.iterdir()]

            if stations:
                stations_to_process = [station + ".csv" for station in stations]
            else:
                stations_to_process = available_stations

            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            plt.figure(figsize=(20, 12))

            for station in stations_to_process:
                station_path = datadir / station
                if not station_path.exists():
                    self.logger.warning("Stacja '%s' nie istnieje.", station_path)
                    continue

                df = pd.read_csv(station_path, usecols=["Data", parameter], encoding=Dirs.ENCODING)
                df["Data"] = pd.to_datetime(df["Data"])

                df = df[df["Data"] >= start_date]
                df = df[df["Data"] <= end_date]

                self.logger.debug("Dane dla stacji '%s':\n%s", station, df)
                if df.empty:
                    self.logger.warning("Brak danych do wyświetlenia dla stacji '%s' w podanym zakresie czasu.", station)
                    continue

                sns.lineplot(data=df, x="Data", y=parameter, label=f"Stacja {station}")

            plt.title(f"Wykres szeregów czasowych dla '{parameter}'")
            plt.xlabel("Data")
            plt.ylabel(parameter)
            plt.xticks(rotation=45)
            plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))  # Ograniczenie liczby etykiet na osi X
            plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.)
            temp = self.output_dir / data_type
            temp.mkdir(parents=True, exist_ok=True)

            output_file = self.output_dir / data_type / f"{data_type}_multi_{parameter.replace('/', '_')}.png"
            plt.savefig(output_file, bbox_inches="tight")
            plt.close()
            self.logger.info("Zapisano wykres do pliku: %s", output_file)

    def plot_distribution(self, data_type: str, parameters: list[str], start_date: str, end_date: str, stations: list[str] = None) -> None:
        """Tworzy histogram oraz wykres pudełkowy dla wybranych parametrów, porównując podane stację na wykresie.

        Args:
            data_type (str): Typ danych.
            parameters (list[str], optional): Nazwy parametrów do analizy.
            start_date (str): Początkowa data w formacie 'YYYY-MM-DD'.
            end_date (str): Końcowa data w formacie 'YYYY-MM-DD'.
            stations (list[str], optional): Lista ID stacji. Jeśli None, wykresy są tworzone dla wszystkich stacji.

        Returns:
            None
        """
        if parameters == []:
            self.logger.info("Analiza dla wszystkich parametrów")
            parameters = self.parameter_map[data_type]

        for parameter in parameters:
            if parameter not in self.parameter_map[data_type]:
                self.logger.error("Parametr '%s' nie jest dostępny dla typu danych '%s'.", parameter, data_type)
                return
            datadir = Path(self.data_dir / data_type)
            available_stations = [d.name for d in datadir.iterdir()]

            if stations:
                stations_to_process = [station + ".csv" for station in stations]
            else:
                stations_to_process = available_stations

            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            plt.figure(figsize=(15, 10))

            all_data = []
            for station in stations_to_process:
                station_path = datadir / station
                if not station_path.exists():
                    self.logger.warning("Stacja '%s' nie istnieje.", station_path)
                    continue

                df = pd.read_csv(station_path, usecols=["Data", parameter], encoding=Dirs.ENCODING)
                df["Data"] = pd.to_datetime(df["Data"])
                df = df[df["Data"] >= start_date]
                df = df[df["Data"] <= end_date]

                if df.empty:
                    self.logger.warning("Brak danych do wyświetlenia dla stacji '%s' w podanym zakresie czasu.", station)
                    continue

                df["Stacja"] = station  # Dodaj kolumnę z nazwą stacji
                all_data.append(df)

            if not all_data:
                self.logger.warning("Brak danych do wyświetlenia dla żadnej stacji w podanym zakresie czasu.")
                return

            combined_df = pd.concat(all_data)

            # Tworzenie wykresu histogramu
            plt.figure(figsize=(15, 10))
            sns.histplot(data=combined_df, x=parameter, hue="Stacja", multiple="stack")
            plt.title(f"Histogram dla '{parameter}'")
            plt.xlabel(parameter)
            plt.ylabel("Liczba wystąpień")
            plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.)

            plt.tight_layout()
            output_file_hist = self.output_dir / data_type / f"{data_type}_hist_{parameter.replace('/', '_')}.png"
            plt.savefig(output_file_hist, bbox_inches="tight")
            plt.close()
            self.logger.info("Zapisano histogram do pliku: %s", output_file_hist)

            # Tworzenie wykresu pudełkowego
            plt.figure(figsize=(20, 12))
            sns.boxplot(data=combined_df, x="Stacja", y=parameter)
            plt.title(f"Wykres pudełkowy dla '{parameter}'")
            plt.xlabel("Stacja")
            plt.ylabel(parameter)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.)
            output_file = self.output_dir / data_type / f"{data_type}_distribution_{parameter.replace('/', '_')}.png"
            plt.savefig(output_file, bbox_inches="tight")
            plt.close()
            self.logger.info("Zapisano wykresy rozkładu do pliku: %s", output_file)
