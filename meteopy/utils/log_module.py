import logging
from pathlib import Path
from meteopy.consts.dirs import Dirs

def get_logger(name: str, log_file: Path = Dirs.LOG_DIR / "app.log", level: int = logging.INFO) -> logging.Logger:
    """
    Konfiguruje logger dla aplikacji.

    Args:
        name (str): Nazwa loggera (zazwyczaj modułu).
        log_file (Path): Ścieżka do pliku logów.
        level (int): Poziom logowania (np. logging.INFO).

    Returns:
        logging.Logger: Skonfigurowany logger.
    """
    # Upewnij się, że katalog dla logów istnieje
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Konfiguracja loggera
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Formatter dla logów
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Stream handler (opcjonalnie można wyświetlać logi na konsoli)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Dodawanie handlerów do loggera
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger