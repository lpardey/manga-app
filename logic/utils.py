# Standard Library
import platform
from pathlib import PurePath


class DownloaderException(Exception):
    pass


class DownloaderExceptionUrlWithoutCoverage(DownloaderException):
    def __init__(self, message: str = "URL not registered in MangaDanga!") -> None:
        self.message = message
        super().__init__(self.message)


class DownloaderExceptionInvalidPattern(DownloaderException):
    def __init__(
        self,
        message: str = "Invalid argument pattern. A valid pattern consists of two numbers where first one is smaller than the second ,e.g., '1-8'",
    ) -> None:
        self.message = message
        super().__init__(self.message)


class DownloaderExceptionUnexpected(DownloaderException):
    pass


def get_forbidden_chars() -> set[str] | None:
    operating_system = platform.system()
    os_to_forbidden_chars = {
        "Windows": {"/", ">", "<", ":", '"', "\\", "|", "?", "*", " "},
        "Linux": {"/", " "},
        "Darwin": {"/", ":", " "},
    }
    return os_to_forbidden_chars[operating_system] if operating_system in os_to_forbidden_chars else None


def format_name(name: str) -> str:
    forbidden_chars = get_forbidden_chars()
    if not forbidden_chars:
        return name
    formatted_name = ""
    for char in name.strip():
        if char in forbidden_chars:
            formatted_name += "_"
        else:
            formatted_name += char
    return formatted_name


def get_src_numbers_suffix(src: str) -> str:
    src_stem = PurePath(src).stem
    suffix = []
    for character in reversed(src_stem):
        if character.isnumeric():
            suffix.append(character)
        else:
            break
    suffix.reverse()
    src_numbers_suffix = "".join(suffix)
    return src_numbers_suffix
