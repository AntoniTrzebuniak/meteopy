from __future__ import annotations

import random

import click

from meteopy.consts import Dirs
from meteopy.eda.imgw_eda_visualizer import IMGWDataVisualizer
from meteopy.statistics.imgw_stats import IMGWStats
from meteopy.utils.log_module import get_logger

logger = get_logger(__name__)


@click.command()
@click.argument("data_type", type=int)
def basic_summary(data_type: int) -> None:
    """
        Generates basic statistics for selected parameters based on user input.

    SYNOPSIS
        basic_summary(data_type: int)

    PARAMETERS
        data_type (int)
        The type of data for which statistics are to be generated.
        Valid values are 1 - klimat, 2 - opad, or 3 - synop.

    DESCRIPTION
        Generates basic statistics for selected parameters based on user input.

        The function performs the following steps:\n
        1. Validates the provided data type.\n
        2. Retrieves the list of parameters associated with the data type.\n
        3. Displays the list of parameters for the user to choose from.\n
        4. Prompts the user to select a parameter from the list.\n
        5. Validates the selected parameter.\n
        6. Retrieves available station paths for the given data type.\n
        7. Randomly selects 5 stations (or fewer if less than 5 are available).\n
        8. Processes data for each selected station and generates statistics.

        If any errors occur during the process (e.g., invalid data type or parameter selection),
        appropriate error messages are logged.

        Note: Data should be downloaded and preprocessed before running this function.
    Returns:
        None
    """
    try:
        data_type_str = Dirs.DATA_TYPES[data_type - 1]
    except IndexError:
        logger.error("Niepoprawny typ danych. Wybierz 1, 2 lub 3.")
        return

    parameter_list = Dirs.PARAMETER_MAP.get(data_type_str, [])
    if not parameter_list:
        logger.error("Brak parametrów dla typu danych: %s", data_type_str)
        return

    selected_parameters = []
    for idx, param in enumerate(parameter_list, start=1):
        click.echo(f"{idx}. {param}")
    while True:
        parameter_index = click.prompt("Wybierz number parametru z listy (0 aby zakończyć)", type=int)
        if parameter_index == 0:
            break
        try:
            parameter = parameter_list[parameter_index - 1]
            selected_parameters.append(parameter)
        except IndexError:
            logger.error("Niepoprawny numer parametru. Wybierz numer od 1 do %d.", len(parameter_list))
            continue

    if not selected_parameters:
        logger.error("Nie wybrano żadnych parametrów.")
        return
    click.echo("wybierz zakres lat na wykresie")
    start_year = click.prompt("Podaj rok początkowy", type=int)
    end_year = click.prompt("Podaj rok końcowy", type=int)
    start = f"{start_year}-01-01"
    end = f"{end_year}-12-31"

    logger.info("Generowanie statystyk dla typu danych: %s", data_type_str)
    station_paths = Dirs.get_available_stations_paths(data_type_str)
    random_stations = random.sample(station_paths, min(5, len(station_paths)))
    random_stations = [ station.name.replace(".csv","") for station in random_stations]
    logger.info("Wybrane parametry: %s", ", ".join(selected_parameters))
    stats = IMGWStats()
    stats.calculate_basic_stat(data_type_str, selected_parameters, random_stations)
    visualizer = IMGWDataVisualizer()

    for station_path in random_stations:
        visualizer.plot_time_series(data_type_str, selected_parameters, start, end, [station_path])
        visualizer.distribution_polts(data_type_str, selected_parameters, start, end, [station_path])
    logger.info("Generowanie statystyk zakończone.")
