from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from meteopy.utils.log_module import get_logger
from meteopy.consts.dirs import Dirs


class IMGWSimpleForecaster:
    def __init__(self):
        self.model = LinearRegression()
        self.logger = get_logger(__name__)

    def linear_regression_forecast(self, data_type: str, start_date: str, end_date: str, till_predict_date: str, stations: list[str], parameter: str):
        """Tworzy prosty model regresji liniowej do przewidywania wartości na podstawie danych historycznych.
        Args:
            data_type: Typ danych (np. 'temperature')
            start_date: Data początkowa w formacie 'YYYY-MM-DD'
            end_date: Data końcowa w formacie 'YYYY-MM-DD'
            till_predict_date: Data do której przewidujemy wartości w formacie 'YYYY-MM-DD'
            stations: Lista stacji do uwzględnienia
            parameter: Parameter do przewidywania
        Returns:
            Przewidywane wartości na podstawie modelu regresji liniowej

        """
        for station in stations:
            
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            till_predict_date = pd.to_datetime(till_predict_date)
            
            parameter_list = Dirs.PARAMETER_MAP.get(data_type)
            if parameter not in parameter_list:
                raise ValueError(f"Parameter {parameter} nie jest obsługiwany.")
            
            file_path = os.path.join(Dirs.SEPARATED_DIR, data_type, f"{station}.csv")
            df = pd.read_csv(file_path, encoding=Dirs.ENCODING)
            
            df["Data"] = pd.to_datetime(df["Data"])
            df = df[df["Data"] >= start_date]
            df = df[df["Data"] <= end_date]
            
            # Przygotowanie danych treningowych           
            filtered_data = df[["Data", parameter]].dropna()
            filtered_data["date"] = pd.to_datetime(filtered_data["Data"])
            X_train = filtered_data["date"].map(lambda x: x.toordinal()).values.reshape(-1, 1)
            y_train = filtered_data[parameter].values
                        
            # Przygotowanie danych do przewidywania
            X_predict_dates = pd.date_range(start=end_date, end=till_predict_date, freq="D")
            X_predict = X_predict_dates.to_series().map(lambda x: x.toordinal()).values.reshape(-1, 1)

            if X_train.shape[0] == 0 or y_train.shape[0] == 0:
                self.logger.error("Found array with 0 sample(s) while a minimum of 1 is required by LinearRegression.")
                return None, None, None, None, None

            # Dopasowanie modelu do danych treningowych
            self.model.fit(X_train, y_train)

            # Przewidywanie wartości na podstawie modelu
            predictions = self.model.predict(X_predict)

            return X_train, y_train, X_predict_dates, predictions, filtered_data

    def plot_forecast(self, data_type: str, start_date: str, end_date: str, till_predict_date: str, stations: list[str], parameter: str):
        """Tworzy wykres wartości użytych do trenowania modelu oraz wartości przewidywanych.

        Args:
            data_type: Typ danych (np. 'temperature')
            start_date: Data początkowa w formacie 'YYYY-MM-DD'
            end_date: Data końcowa w formacie 'YYYY-MM-DD'
            till_predict_date: Data do której przewidujemy wartości w formacie 'YYYY-MM-DD'
            stations: Lista stacji do uwzględnienia
            parameter: Parameter do przewidywania

        """
        if not stations:
            data_dir = os.path.join(Dirs.SEPARATED_DIR, data_type)
            stations = [os.path.splitext(file)[0] for file in os.listdir(data_dir) if file.endswith(".csv")]

        for station in stations:
            X_train, y_train, X_predict_dates, predictions, filtered_data = self.linear_regression_forecast(
                data_type, start_date, end_date, till_predict_date, [station], parameter
            )

            if X_train is None or y_train is None:
                self.logger.error("Training data is empty. Skipping forecast plot.")
                return

            plt.figure(figsize=(15, 10))
            plt.plot(filtered_data["date"], y_train, label="Dane historyczne")
            plt.plot(X_predict_dates, predictions, label="Przewidywania", linestyle="--")
            plt.xlabel("Data")
            plt.ylabel(parameter)
            plt.title(f"Przewidywania dla stacji {station}")
            plt.legend()
            plt.xticks(rotation=45)

            output_dir = os.path.join(Dirs.FORECAST_DIR, data_type)
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{station}_{parameter}_forecast.png")
            plt.savefig(output_file, bbox_inches="tight")
            plt.close()
            print(f"Zapisano wykres do pliku: {output_file}")
