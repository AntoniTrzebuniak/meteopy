
from __future__ import annotations
import logging
from pathlib import Path

from meteopy.consts.dirs import Dirs


def get_logger(name: str, log_file: Path = Dirs.LOG_DIR / "app.log", level: int = logging.INFO) -> logging.Logger:
    """Konfiguruje logger dla aplikacji.

    Args:
        name (str): Nazwa loggera (zazwyczaj modułu).
        log_file (Path): Ścieżka do pliku logów.
        level (int): Poziom logowania (np. logging.INFO).

    Returns:
        logging.Logger: Skonfigurowany logger.

    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

def get_logger(
        name: str,
        log_lvl: int = logging.DEBUG,   ) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_lvl)

    if not logger.handlers:
        formatter = logging.Formatter(fmt="%(asctime)s : %(name)s : %(levelname)s : %(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger