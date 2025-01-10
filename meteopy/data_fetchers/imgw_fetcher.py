import os
import requests
import zipfile
from pathlib import Path
from meteopy.consts.dirs import Dirs


class IMGWDataFetcher:
    """
    Klasa do pobierania danych meteorologicznych z IMGW.
    """

    def __init__(self):
        self.download_dir = Dirs.DATA_DIR / "downloaded"
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def fetch(self, catalog_url: str, file_pattern: str):
        """
        Przeszukuje katalog pod kątem plików pasujących do wzorca.

        Args:
            catalog_url (str): URL katalogu do przeszukiwania.
            file_pattern (str): Wzorzec plików do wyszukiwania.

        Returns:
            list[str]: Lista znalezionych plików pasujących do wzorca.
        """
        response = requests.get(catalog_url)
        response.raise_for_status()

        # Zakładając, że katalog to lista plików (np. HTML lub JSON)
        files = response.text.splitlines()
        matching_files = [file for file in files if file_pattern in file]

        return matching_files

    def download_file(self, file_url: str, unzip: bool = False):
        """
        Pobiera plik pod wskazanym URL i opcjonalnie go rozpakowuje.

        Args:
            file_url (str): URL pliku do pobrania.
            unzip (bool): Czy plik powinien zostać wypakowany (jeśli jest archiwum ZIP).
        """
        local_filename = self.download_dir / Path(file_url).name

        with requests.get(file_url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        if unzip and zipfile.is_zipfile(local_filename):
            with zipfile.ZipFile(local_filename, 'r') as zip_ref:
                zip_ref.extractall(self.download_dir)