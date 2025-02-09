import os
import shutil
import click
from meteopy.consts.dirs import Dirs


@click.command()
def drop_data() -> None:
    """Usuwa wszystkie pobrane dane.

    Funkcja próbuje usunąć katalog data/separated/ oraz wszystkie pliki i podkatalogi w nim zawarte.
    Jeśli operacja się powiedzie, wyświetla komunikat o sukcesie. W przeciwnym razie, wyświetla
    komunikat o błędzie z podaniem przyczyny niepowodzenia.

    Wyjątki:
        W przypadku wystąpienia błędu podczas usuwania katalogu, wyjątek jest przechwytywany i
        wyświetlany jest komunikat o błędzie.

    Zwraca:
        None

    """

    try:
        shutil.rmtree(Dirs.SEPARATED_DIR)
        print(f'Successfully deleted {Dirs.SEPARATED_DIR}')
    except Exception as e:
        print(f'Failed to delete {Dirs.SEPARATED_DIR}. Reason: {e}')
