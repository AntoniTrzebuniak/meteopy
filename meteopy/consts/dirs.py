from __future__ import annotations

from pathlib import Path


class Dirs:
    ROOT_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = ROOT_DIR/"data"/"downloaded"
    LOG_DIR = ROOT_DIR / "logs"
    IMGW_URL = 'https://danepubliczne.imgw.pl/data/arch/ost_hydro/123'
    @staticmethod
    def get_data_path():
        '''Returns the path to the data directory.'''
        if not Dirs.DATA_DIR.exists():
            raise FileNotFoundError(
                f"Katalog '{Dirs.DATA_DIR}' nie istnieje. Upewnij się, że został utworzony poprawnie."
            )
        if not Dirs.DATA_DIR.is_dir():
            raise NotADirectoryError(
                f"Ścieżka '{Dirs.DATA_DIR}' istnieje, ale nie jest katalogiem. Usuń plik lub zmień konfigurację."
            )
        
        return Dirs.DATA_DIR
        

    @staticmethod
    def get_log_path(filename: str) -> Path:   
        return Dirs.LOG_DIR / filename
    
    @staticmethod
    def get_root_path() -> Path:
        return Dirs.ROOT_DIR
    