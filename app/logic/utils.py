# Standard Library
import platform


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
