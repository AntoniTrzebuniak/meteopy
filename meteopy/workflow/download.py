from __future__ import annotations

import click

from meteopy.data_fetchers.imgw_fetcher import KODataFetcher, SynopDataFetcher
from meteopy.preprocessing.imgw_handler import IMGWDataHandler
from meteopy.utils.log_module import get_logger

logger = get_logger(__name__)


@click.command()
def download():
    """Przeprowadź cały proces pobierania i przetwarzania danych krok po kroku."""
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


def fetch_data(start_year, end_year, data_type):
    """Funkcja do pobierania danych."""
    if data_type == 1 or data_type == 2:
        fetcher = KODataFetcher()
    elif data_type == 3:
        fetcher = SynopDataFetcher()
    fetcher.fetch(start_year, end_year, data_type)
    print(f"Dane zostały pobrane dla lat {start_year}-{end_year} i typu {data_type}.")


def preprocess_data(missing_data_strategy):
    """Funkcja do przetwarzania danych."""
    handler = IMGWDataHandler()
    handler.divide_downloaded()
    handler.preprocess(missing_data_strategy)
    print(f"Dane zostały przetworzone z użyciem strategii: {missing_data_strategy}.")
