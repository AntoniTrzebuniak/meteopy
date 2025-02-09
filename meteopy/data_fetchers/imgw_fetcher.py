from __future__ import annotations

import re
import zipfile
from abc import ABC, abstractmethod
from pathlib import Path

import requests

from meteopy.consts.dirs import Dirs
from meteopy.utils.log_module import get_logger


class IMGWDataFetcher(ABC):
    def __init__(self):
        self.data_dir = Dirs.DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = Dirs.IMGW_URL
        self.dataType = ["klimat", "opad", "synop"]
        self.logger = get_logger("IMGWDataFetcher")

    def open_site(self, URL, unzip: bool = True):
        response = requests.get(URL)
        if response.status_code != requests.codes.ok:
            self.logger.critical(f"response.status_code: {response.status_code} Nieprawidłowy address URL")
        else:
            self.logger.debug(f"response.status_code: {response.status_code} Poprawnie otwarto stronę {Path(URL).name}")
        return response.text

    def download_dir(self, URL: str, unzip: bool = True):
        """Pobiera zawartość katalogu i opcjonalnie nie rozpakowuje zipów."""
        content = self.open_site(URL)
        zips = re.findall(r'href="([^"]+)"', content)
        zips = [zipp for zipp in zips if zipp.endswith(".zip")]
        for zipp in zips:
            self.download_file(URL + zipp, True)

    def download_file(self, file_url: str, unzip: bool = False):
        """Pobiera plik pod wskazanym URL i opcjonalnie go rozpakowuje.

        Args:
            file_url (str): URL pliku do pobrania.
            unzip (bool): Czy plik powinien zostać wypakowany (jeśli jest archiwum ZIP).

        """
        local_filename = self.tempdata_dir / Path(file_url).name
        with requests.get(file_url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        self.logger.debug(f"Pobieranie zakończone: {local_filename}")
        if unzip and zipfile.is_zipfile(local_filename):
            with zipfile.ZipFile(local_filename, "r") as zip_ref:
                zip_ref.extractall(self.tempdata_dir)
            local_filename.unlink()

    def cleanup(self) -> None:
        """Usuwa pliki zaczynające się na 's_d_' i 'k_d_t' z folderu Dirs.DATA_DIR."""
        for directory in self.data_dir.iterdir():
            for file_path in directory.glob("*.csv"):
                if file_path.is_file() and self.should_delete_file(file_path.name):
                    try:
                        file_path.unlink()
                        self.logger.debug("Usunięto plik: %s", file_path)
                    except Exception:
                        self.logger.exception("Błąd podczas usuwania pliku %s", file_path)

    @staticmethod
    def should_delete_file(file_name: str) -> bool:
        """Sprawdza, czy plik powinien zostać usunięty."""
        if (file_name.startswith("k_d_t")) or (
            file_name.startswith("s_d_") and (not file_name.startswith("s_d_t"))
        ):  # te pliki usunięte
            return True
        return False

    @abstractmethod
    def fetch(self, startYear: int, endYear: int, typdanych: int):
        pass


class KODataFetcher(IMGWDataFetcher):
    """Klasa do pobierania danych meteorologicznych z IMGW."""

    def __init__(self):
        super().__init__()

    def fetch(self, startYear: int, endYear: int, typdanych: int):
        """Szuka."""
        if typdanych == 3:
            self.logger.critical("przekazano zły typ danych (synop) do KO ")
        self.tempdata_dir = Dirs.DATA_DIR / self.dataType[typdanych - 1]
        if not self.tempdata_dir.exists():
            self.tempdata_dir.mkdir(parents=True, exist_ok=True)
        Current_URL = self.base_url + self.dataType[typdanych - 1] + "/"

        page_content = self.open_site(Current_URL)
        folders = re.findall(r'href="([^"]+)"', page_content)

        folders = [folder for folder in folders if folder.endswith("/")]
        folders = [item for item in folders if re.compile(r"\d").search(item)]

        for folder in folders:
            match_range = re.match(r"(\d{4})_(\d{4})/", folder)
            match_single = re.match(r"(\d{4})/", folder)

            if match_single:
                folder_year = int(match_single.group(1))
                if startYear <= folder_year:
                    if folder_year > endYear:
                        break
                    self.download_dir(Current_URL + folder, True)

            elif match_range:
                start, end = map(int, match_range.groups())
                if startYear <= start and end <= endYear:
                    self.download_dir(Current_URL + folder, True)

                elif start <= endYear and end >= startYear:
                    content = self.open_site(Current_URL + folder)
                    zips = re.findall(r'href="([^"]+)"', content)
                    zips = [zipp for zipp in zips if zipp.endswith(".zip")]
                    for zipp in zips:
                        match = re.match(r"^(\d{4})", zipp)  # Dopasowanie roku na początku nazwy
                        if match:
                            year = int(match.group(1))  # Konwersja roku na liczbę całkowitą
                            if startYear <= year <= endYear:
                                self.download_file(Current_URL + folder + zipp, True)
        self.cleanup()


class SynopDataFetcher(IMGWDataFetcher):
    """Klasa do pobierania danych meteorologicznych z IMGW."""

    def __init__(self):
        super().__init__()

    def fetch(self, startYear: int, endYear: int, typdanych: int = 3):
        """Szuka."""
        if typdanych != 3:
            self.logger.critical("przekazano zły typ danych (opad lub klimat) do Synop ")
        self.tempdata_dir = Dirs.DATA_DIR / self.dataType[typdanych - 1]
        if not self.tempdata_dir.exists():
            self.tempdata_dir.mkdir(parents=True, exist_ok=True)
        Current_URL = self.base_url + self.dataType[typdanych - 1] + "/"

        page_content = self.open_site(Current_URL)
        folders = re.findall(r'href="([^"]+)"', page_content)

        folders = [folder for folder in folders if folder.endswith("/")]
        folders = [item for item in folders if re.compile(r"\d").search(item)]

        for folder in folders:
            match_range = re.match(r"(\d{4})_(\d{4})/", folder)
            match_single = re.match(r"(\d{4})/", folder)

            if match_single:
                folder_year = int(match_single.group(1))
                if startYear <= folder_year:
                    if folder_year > endYear:
                        break
                    self.download_dir(Current_URL + folder)
            elif match_range:
                start, end = map(int, match_range.groups())
                if start <= endYear and end >= startYear:
                    self.download_dir(Current_URL + folder)
        self.cleanup()
