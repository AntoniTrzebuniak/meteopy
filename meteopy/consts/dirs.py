from pathlib import Path

class Dirs:
    ROOT_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = ROOT_DIR / "data"
    LOG_DIR = ROOT_DIR / "logs"

