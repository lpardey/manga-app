# Local imports
from ..downloader.exceptions import DownloaderException

WINDOWS_ICON_RAW_PATH = r"C:\Users\lpard\repos\manga-app\mangadanga\gui\static\Guts.ico"



def validate_non_empty(field: str, name: str) -> None:
    if not field:
        raise DownloaderException(f"'{name}' is missing.")


def validate_numeric(field: str, name: str) -> None:
    try:
        float(field)
    except ValueError:
        raise DownloaderException(f"'{name}' must be numeric.")
