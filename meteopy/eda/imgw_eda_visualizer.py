from __future__ import annotations

from pathlib import Path
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from meteopy.consts.dirs import Dirs
from meteopy.utils.log_module import get_logger


class IMGWDataVisualizer:

    def __init__(self):
        
        Dirs.PLOTS_DIR.mkdir(parents=True, exist_ok=True)
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
        OUTPUT_DIR = Dirs.PLOTS_DIR/data_type
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        if parameters == []:
            self.logger.info("Analiza dla wszystkich parametrów")
            parameters = self.parameter_map[data_type]

        for parameter in parameters:
            if parameter not in self.parameter_map[data_type]:
                self.logger.error("HALT: Parameter '%s' nie jest dostępny dla typu danych '%s'.", parameter, data_type)
                return
            
        datadir = Path( Dirs.SEPARATED_DIR / data_type)
        if not datadir.exists():
            self.logger.error("nie ma danych dla wybranego typu")
            return
            
        if stations:
            stations_to_process = [station + ".csv" for station in stations]
        else:
            stations_to_process = [d.name for d in datadir.iterdir()]



        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        figures = [plt.figure(figsize=(20, 12)) for _ in parameters]
        axes = [fig.add_subplot(111) for fig in figures]

        for station in stations_to_process:
            self.logger.debug(f"analizowanie {station}")
            station_path = datadir / station
            if not station_path.exists():
                self.logger.warning("Stacja '%s' nie istnieje.", station_path)
                continue

            usecols = ["Nazwa_stacji", "Data"] + parameters
            df = pd.read_csv(station_path, usecols=usecols, encoding=Dirs.ENCODING)
            df["Data"] = pd.to_datetime(df["Data"])

            df = df[df["Data"] >= start_date]
            df = df[df["Data"] <= end_date]

            if df.empty:
                self.logger.warning("Brak danych do wyświetlenia dla stacji '%s' w podanym zakresie czasu.", station)
                continue

            for parameter, ax in zip(parameters, axes):
                sns.lineplot(data=df, x="Data", y=parameter, label=f"{df["Nazwa_stacji"][0]}", ax=ax)
                ax.set_title(f"Wykres szeregów czasowych dla '{parameter}'")
                ax.set_xlabel("Data")
                ax.set_ylabel(parameter)
                ax.xaxis.set_major_locator(plt.MaxNLocator(10))  # Ograniczenie liczby etykiet na osi X
                ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.)

        for fig, parameter in zip(figures, parameters):
            output_file = OUTPUT_DIR / f"{data_type}_multi_{parameter.replace('/', '_')}.png"
            warnings.filterwarnings("ignore", category=UserWarning)
            fig.savefig(output_file, bbox_inches="tight")
            plt.close(fig)
            self.logger.info("Zapisano wykres do pliku: %s", output_file)

        

    def distribution_polts(self, data_type: str, parameters: list[str], start_date: str, end_date: str, stations: list[str] = None) -> None:
        """Tworzy histogram oraz wykres pudełkowy dla wybranych parametrów, porównując podane stację na jednym wykresie.

        Args:
            data_type (str): Typ danych.
            parameters (list[str], optional): Nazwy parametrów do analizy.
            start_date (str): Początkowa data w formacie 'YYYY-MM-DD'.
            end_date (str): Końcowa data w formacie 'YYYY-MM-DD'.
            stations (list[str], optional): Lista ID stacji. Jeśli None, wykresy są tworzone dla wszystkich stacji.

        Returns:
            None

        """
        OUTPUT_DIR = Dirs.PLOTS_DIR/data_type
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        if parameters == []:
            self.logger.info("Analiza dla wszystkich parametrów")
            parameters = self.parameter_map[data_type]

        for parameter in parameters:
            if parameter not in self.parameter_map[data_type]:
                self.logger.error("Parameter '%s' nie jest dostępny dla typu danych '%s'.\n KOŃCZENIE DZIALANIA FUNKCJI", parameter, data_type)
                return
        datadir = Path(Dirs.SEPARATED_DIR / data_type)

        if stations:
            stations_to_process = [station + ".csv" for station in stations]
        else:
            stations_to_process = [d.name for d in datadir.iterdir()]

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        plt.figure(figsize=(15, 10))

        all_data = []
        for station in stations_to_process:
            station_path = datadir / station
            if not station_path.exists():
                self.logger.warning("Stacja '%s' nie istnieje.", station_path)
                continue
            
            cols_to_read = ["Kod_stacji", "Nazwa_stacji", "Data"] +  parameters
            df = pd.read_csv(station_path, usecols=cols_to_read, encoding=Dirs.ENCODING)
            df["Data"] = pd.to_datetime(df["Data"])
            df = df[df["Data"] >= start_date]
            df = df[df["Data"] <= end_date]

            if df.empty:
                self.logger.warning("Brak danych do wyświetlenia dla stacji '%s' w podanym zakresie czasu.", station)
                continue

            all_data.append(df)

        if not all_data:
            self.logger.warning("Brak danych do wyświetlenia dla żadnej stacji w podanym zakresie czasu.")
            return

        combined_df = pd.concat(all_data, ignore_index=True)
        #combined_df.to_csv( self.output_dir / data_type, encoding= Dirs.ENCODING, index=False)
        
        for parameter in parameters:
        # Tworzenie wykresu histogramu
            plt.figure(figsize=(15, 10))
            sns.histplot(data=combined_df, x=parameter, hue="Nazwa_stacji", multiple="stack", element="step", edgecolor=None, legend=False )
            plt.title(f"Histogram dla '{parameter}'")
            plt.xlabel(parameter)
            plt.ylabel("Liczba wystąpień")
        
            plt.tight_layout()
            output_file_hist = Dirs.PLOTS_DIR / data_type / f"Hist_{parameter.replace('/', '_')}_{data_type}.png"
            plt.savefig(output_file_hist, bbox_inches="tight")
            plt.close()
            self.logger.info("Zapisano histogram do pliku: %s", output_file_hist)

            # Tworzenie wykresu pudełkowego
            plt.figure(figsize=(20, 12))
            sns.boxplot(data=combined_df, x="Nazwa_stacji", y=parameter, legend=False)
            plt.title(f"Wykres pudełkowy dla '{parameter}'")
            plt.xlabel("Stacja")
            plt.ylabel(parameter)
            plt.xticks(rotation=45)
            plt.tight_layout()
            #plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.)
            output_file = Dirs.PLOTS_DIR / data_type / f"Distribution_{parameter.replace('/', '_')}_{data_type}.png"
            warnings.filterwarnings("ignore", category=UserWarning)
            plt.savefig(output_file, bbox_inches="tight")
            plt.close()
            self.logger.info("Zapisano wykresy rozkładu do pliku: %s", output_file)
