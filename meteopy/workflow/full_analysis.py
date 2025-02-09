from __future__ import annotations

import click

from meteopy.consts import Dirs
from meteopy.eda.imgw_eda_visualizer import IMGWDataVisualizer
from meteopy.forecasting.imgw_simple_forecaster import IMGWSimpleForecaster
from meteopy.statistics.imgw_stats import IMGWStats
from meteopy.utils.log_module import get_logger
from meteopy.workflow.download import fetch_data, preprocess_data

logger = get_logger(__name__)


@click.command()
def full_analysis():
    """Przeprowadź cały process pobierania i wygeneruje wszystkie wykresy dla wszystkich stacji dla wszystkich
    parametrów (UWAGA: może to potrwać dłuższą chwilę i zająć nawet 10GB RAMU (dla 1000 stacji), gdyż wsystkie stację są
    nanoszone na jeden wykres dla IMGWDataVisualizer)."""
    start_year = click.prompt("Podaj rok początkowy", type=int)
    end_year = click.prompt("Podaj rok końcowy", type=int)
    data_type = click.prompt("Podaj typ danych: 1 - klimat, 2 - opad, 3 - synop", type=int)
    if data_type not in [1, 2, 3]:
        logger.error("Typ danych musi być jednym z: 1 - klimat, 2 - opad, 3 - synop")
        logger.info("zastosowano domyślną wartość 1")
        data_type = 1

    click.echo("Pobieranie danych...")
    fetch_data(start_year, end_year, data_type)
    click.echo("Pobieranie zakończone.")

    missing_data_strategy = click.prompt("Podaj strategię radzenia sobie z brakami danych:\n1 - zostawia brakujące dane bez zmian,\n2 - uzupełnia brakujące dane wartością z poprzedniego dnia,\n3 - uzupełnia brakujące dane średnią z 50 poprzednich dni", type=int)
    if missing_data_strategy not in [1, 2, 3]:
        raise click.BadParameter("Strategia radzenia sobie z brakami danych musi być jednym z: 1, 2, 3")

    click.echo("Przetwarzanie danych...")
    preprocess_data(missing_data_strategy)
    click.echo("Przetwarzanie zakończone.")

    Start_date = f"{start_year}-01-01"
    End_date = f"{end_year}-12-31"
    visualizer = IMGWDataVisualizer()
    forecaster = IMGWSimpleForecaster()
    stats = IMGWStats()
    typ = Dirs.DATA_TYPES[data_type - 1]

    visualizer.plot_time_series(data_type=typ, parameters=[],
                                start_date=Start_date, end_date=End_date, stations=[])

    visualizer.plot_distribution(data_type=typ, parameters=[],
                                start_date=Start_date, end_date=End_date, stations=[])

    #stats.calculate_correlation([], typ, Dirs.PARAMETER_MAP[typ][0], Dirs.PARAMETER_MAP[typ][1])
    stats.calculate_basic_stat([], typ, Dirs.PARAMETER_MAP[typ])

    for i in range(len(Dirs.PARAMETER_MAP[typ])):
        forecaster.plot_forecast(typ, Start_date, End_date, f"{end_year + 1}-12-31", [], Dirs.PARAMETER_MAP[typ][i])
