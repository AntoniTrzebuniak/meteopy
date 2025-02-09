from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from meteopy.consts.dirs import Dirs
from meteopy.utils.log_module import get_logger


class IMGWStats:
    def __init__(self) -> None:
        """Initialize the IMGWStats class."""
        self.logger = get_logger(__name__)

    def calculate_basic_stat(self, stations: list[str], data_type: str, parameters: list[str]) -> None:
        """        Process statistics for the given stations, data type, and parameter,
            and save to a file in data/statistics/<data_type>.
        For each parameter statistics are calculated separately and saved to separate files.

        Args:
stations: List of station IDs to include in the statistics
        data_type: Type of data ['klimat', 'opad', 'synop']
parameters: List of string parameters to calculate statistics for
        Returns:
            None
        """
        if stations == []:
            stations = Dirs.get_available_stations_paths(data_type)

        if parameters == []:
            parameters = Dirs.PARAMETER_MAP.get(data_type)

        for parameter in parameters:
            parameter_list = Dirs.PARAMETER_MAP.get(data_type)
            if not parameter_list or parameter not in parameter_list:
                self.logger.error("Parameter %s not found in PARAMETER_MAP for data type %s", parameter, data_type)
                return

            data_frames = []
            for station in stations:
                file_path = os.path.join(Dirs.SEPARATED_DIR, data_type, f"{station}.csv")
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path, encoding=Dirs.ENCODING)
                    df['station_id'] = station
                    data_frames.append(df)
                else:
                    print(f"File {file_path} does not exist.")
            
            if not data_frames:
                print("No data available for the given stations.")
                return

            data = pd.concat(data_frames, ignore_index=True)
            stats = {}
            for station in stations:
                station_data = data[data['station_id'] == station]
                param_data = station_data[parameter].dropna()
                if param_data.size == 0:
                    self.logger.warning("Brak danych dla parametru '%s'.", parameter)
                    continue
                stats[station] = {
                    'mean': np.mean(param_data),
                    'median': np.median(param_data),
                    'variance': np.var(param_data),
                    'std_dev': np.std(param_data),
                    'quartiles': np.percentile(param_data, [25, 50, 75])
                }

            output_dir = Path(Dirs.STATISTICS_DIR) / data_type
            output_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{parameter}_statistics.txt"
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w') as file:
                for station, param_stats in stats.items():
                    file.write(f"Station: {station}\n")
                    for stat_name, stat_value in param_stats.items():
                        file.write(f"  {stat_name}: {stat_value}\n")
                    file.write("\n")

    def calculate_correlation(self, stations: list[str], data_type: str, parameter1: str, parameter2: str) -> None:
        """Calculate correlation between two parameters for the given stations and data type.

        Args:
            stations: List of station IDs to include in the correlation calculation
            data_type: Type of data ['klimat', 'opad', 'synop']
            parameter1: First parameter for correlation
            parameter2: Second parameter for correlation

        Returns:
            None
        """
        if stations == []:
            stations = Dirs.get_available_stations_paths(data_type)
            stations = [ station.name.replace(".csv","") for station in stations]

        data_frames = []
        for station in stations:
            file_path = os.path.join(Dirs.SEPARATED_DIR, data_type, f"{station}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path, encoding=Dirs.ENCODING)
                df['station_id'] = station
                data_frames.append(df)
            else:
                print(f"File {file_path} does not exist.")
        
        if not data_frames:
            print("No data available for the given stations.")
            return

        data = pd.concat(data_frames, ignore_index=True)
        correlations = {}
        for station in stations:
            station_data = data[data['station_id'] == station]
            param_data1 = station_data[parameter1].dropna()
            param_data2 = station_data[parameter2].dropna()
            if param_data1.size == 0 or param_data2.size == 0:
                self.logger.warning("Brak danych dla parametrów '%s' i '%s' w stacji '%s'.", parameter1, parameter2, station)
                continue
            correlation = np.corrcoef(param_data1, param_data2)[0, 1]
            correlations[station] = correlation

        output_dir = Path(Dirs.STATISTICS_DIR) / data_type
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{parameter1}_{parameter2}_correlation.txt"
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as file:
            for station, correlation in correlations.items():
                file.write(f"Station: {station}\n")
                file.write(f"  Correlation between {parameter1} and {parameter2}: {correlation}\n")
                file.write("\n")

