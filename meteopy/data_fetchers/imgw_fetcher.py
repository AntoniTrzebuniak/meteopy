from __future__ import annotations

import zipfile
from pathlib import Path
import re
import requests

from meteopy.consts.dirs import Dirs


class IMGWDataFetcher:
    """Klasa do pobierania danych meteorologicznych z IMGW."""

    def __init__(self):
        self.download_dir = Dirs.DATA_DIR
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = Dirs.IMGW_URL

    def fetch(self):
        """
        szuka
        """
        print("szukam")
        response = requests.get(self.base_url)
        if response.status_code == 404
            raise 

        if response.status_code == requests.codes.ok:
            page_content = response.text
            folders = re.findall(r'href="([^"]+)"', page_content) #w raw html folder pisze sie < a href =....>
            print(folders)
            folders = [folder for folder in folders if folder.endswith('/')]
            print(folders)
            url = self.url_type(self.parametr)

        '''for year in self.years:
            year_folder = next((folder for folder in folders if re.search(year, folder)), None)
            if year_folder:
                full_url = f"{url}{year_folder}/"
                if self.months:
                    for month in self.months:
                        month_files = [folder for folder in folders if month in folder and year in folder]
                        for m in month_files:
                            full_url = f"{url}{year_folder}{m}"
                            self.download_file(full_url, unzip=True)'''
                            
    def download_file(self, file_url: str, unzip: bool = False):
        """Pobiera plik pod wskazanym URL i opcjonalnie go rozpakowuje.

        Args:
            file_url (str): URL pliku do pobrania.
            unzip (bool): Czy plik powinien zostać wypakowany (jeśli jest archiwum ZIP).

        """
        local_filename = self.download_dir / Path(file_url).name

        with requests.get(file_url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        if unzip and zipfile.is_zipfile(local_filename):
            with zipfile.ZipFile(local_filename, "r") as zip_ref:
                zip_ref.extractall(self.download_dir)

