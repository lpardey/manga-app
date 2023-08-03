# Standard Library
import platform


def format_name(name: str) -> str:
    forbidden_chars = get_forbidden_chars()
    if not forbidden_chars:
        return name
    name = name.strip()
    for char in forbidden_chars:
        name = name.replace(char, "_")
    return name


def get_forbidden_chars() -> set[str]:
    operating_system = platform.system()
    default = {"/", " "}
    os_to_forbidden_chars = {
        "Windows": {"/", ">", "<", ":", '"', "\\", "|", "?", "*", " "},
        "Linux": {"/", " "},
        "Darwin": {"/", ":", " "},
    }
    return os_to_forbidden_chars[operating_system] if operating_system in os_to_forbidden_chars else default
