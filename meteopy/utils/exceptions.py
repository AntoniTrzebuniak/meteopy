class CustomErrors:
    """
    Klasa grupująca niestandardowe wyjątki używane w projekcie.
    """

    ERROR_CODES = {
        100: "Nieznany błąd.",
        101: "Nie udało się pobrać danych.",
        102: "Podano nieprawidłowe dane wejściowe.",
        103: "Błąd podczas przetwarzania pliku.",
        104: "Błąd uwierzytelnienia.",
        105: "Błąd konfiguracji aplikacji.",
    }

    class BaseError(Exception):
        """Bazowy wyjątek dla wszystkich niestandardowych błędów."""
        def __init__(self, code=100, message=None):
            self.code = code
            self.message = message or CustomErrors.ERROR_CODES.get(code, "Nieznany kod błędu.")
            super().__init__(f"[Kod błędu: {self.code}] {self.message}")

    class DataFetchError(BaseError):
        """Wyjątek dla problemów z pobieraniem danych."""
        def __init__(self, message=None):
            super().__init__(code=101, message=message)

    class InvalidInputError(BaseError):
        """Wyjątek dla nieprawidłowych danych wejściowych."""
        def __init__(self, message=None):
            super().__init__(code=102, message=message)

    class FileProcessingError(BaseError):
        """Wyjątek dla błędów związanych z przetwarzaniem plików."""
        def __init__(self, message=None):
            super().__init__(code=103, message=message)

    class AuthenticationError(BaseError):
        """Wyjątek dla błędów uwierzytelnienia."""
        def __init__(self, message=None):
            super().__init__(code=104, message=message)

    class ConfigurationError(BaseError):
        """Wyjątek dla błędów konfiguracji aplikacji."""
        def __init__(self, message=None):
            super().__init__(code=105, message=message)

    @staticmethod
    def raise_error_by_code(code, message=None):
        """
        Funkcja podnosząca wyjątek na podstawie kodu błędu.

        Args:
            code (int): Kod błędu.
            message (str): Opcjonalna wiadomość błędu.

        Raises:
            BaseError: Odpowiedni wyjątek na podstawie kodu.
        """
        error_classes = {
            101: CustomErrors.DataFetchError,
            102: CustomErrors.InvalidInputError,
            103: CustomErrors.FileProcessingError,
            104: CustomErrors.AuthenticationError,
            105: CustomErrors.ConfigurationError,
        }

        error_class = error_classes.get(code, CustomErrors.BaseError)
        raise error_class(message=message)