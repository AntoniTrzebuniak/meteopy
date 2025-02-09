from __future__ import annotations

import logging
from pathlib import Path
from meteopy.consts.dirs import Dirs

def get_logger(name: str, level: int = logging.INFO, log_file: Path = Dirs.LOG_DIR / "app.log") -> logging.Logger:
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
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
