from __future__ import annotations

from pathlib import Path


class Dirs:
    ROOT_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = ROOT_DIR / "data" / "downloaded"
    LOG_DIR = ROOT_DIR / "logs"
    SEPARATED_DIR = ROOT_DIR / "data" / "separated"
    FORECAST_DIR = ROOT_DIR / "data" / "forecast"
    PLOTS_DIR = ROOT_DIR / "data" / "plots"
    STATISTICS_DIR = ROOT_DIR / "data" / "statistics"

    IMGW_URL = "https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/"
    ENCODING = "ISO-8859-2"

    DATA_TYPES = ["klimat", "opad", "synop"]
    PARAMETER_MAP = {
        "klimat": [
            "Maksymalna_temperatura_dobowa_[C]",
            "Minimalna_temperatura_dobowa_[C]",
            "Srednia_temperatura_dobowa_[C]",
            "Temperatura_minimalna_przy_gruncie_[C]",
            "Suma_dobowa_opadow_[mm]",
            "Wysokosc_pokrywy_snieznej_[cm]",
        ],
        "opad": ["Suma_dobowa_opadow_[mm]", "Wysokosc_pokrywy_sniesnej_[cm]", "Wysokosc_swiezospalego_sniegu_[cm]"],
        "synop": [
            "Zachmurzenie_[oktany]",
            "Srednia_dobowa_predkosc_wiatru_[m/s]",
            "Srednia_temperatura_dobowa_[C]",
            "Srednia_dobowe_cisnienie_pary_wodnej_[hPa]",
            "Srednia_dobowa_wilgotnosc_wzgledna_[%]",
            "Srednia_dobowe_cisnienie_na_poziomie_stacji_[hPa]",
            "Srednie_dobowe_cisnienie_na_pozimie_morza_[hPa]",
            "Suma_opadu_dzien_[mm]",
            "Suma_opadu_noc_[mm]",
        ],
    }

    @staticmethod
    def get_available_stations_paths(data_type: str) -> list[str]:
        """Zwraca listę ścierzek dostępnych stacji dla danego typu danych.

        Args:
            data_type (str): Typ danych.

        Returns:
            list[str]: Lista dostępnych stacji.

        """
        datadir = Dirs.SEPARATED_DIR / data_type
        return [d for d in datadir.iterdir()]
