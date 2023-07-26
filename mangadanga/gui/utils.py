from ..downloader.exceptions import DownloaderException


def validate_non_empty(field: str, name: str) -> None:
    if not field:
        raise DownloaderException(f"'{name}' is missing.")


def validate_numeric(field: str, name: str) -> None:
    try:
        float(field)
    except ValueError:
        raise DownloaderException(f"'{name}' must be numeric.")
