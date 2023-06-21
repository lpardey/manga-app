# Standard Library
import urllib.parse
from argparse import ArgumentParser

# Dependencies
from pydantic import BaseModel

# From apps
from logic.utils import DownloaderExceptionInvalidPattern, DownloaderExceptionUrlWithoutCoverage

VALID_URLS = {"chapmanganato.com"}


class MangaDanga(BaseModel):
    name: str = "MangaDanga"
    description: str = "Download your favorite graphic novels by entering its url. A directory named after the novel will be created along with zip files for its chapter/s with its corresponding images. By default, the downloaded files will be stored where you execute the program. Enjoy!"
    epilog: str = "Chachi"
    url_help: str = "Display a url of the graphic novel to download"
    path_help: str = "Display the system path where the files will be stored"
    threads_help: str = "Display a number of threads to use"
    c_help: str = "Display the chapter/s required to download. It takes one or more numbers"
    r_help: str = (
        "Display the range of chapters required to download. It takes two numbers, the first smaller than the second"
    )


def get_parser() -> ArgumentParser:
    program = MangaDanga()
    parser = ArgumentParser(
        prog=program.name,
        description=program.description,
        epilog=program.epilog,
    )
    parser.add_argument("url", help=program.url_help)
    parser.add_argument("-p", "--path", nargs="?", default=".", help=program.path_help)
    parser.add_argument("-t", "--threads", default=0, type=int, help=program.threads_help)
    exclusive_group = parser.add_mutually_exclusive_group()
    exclusive_group.add_argument("-c", "--chapter", nargs="+", type=float, help=program.c_help)
    exclusive_group.add_argument("-r", "--chapter_range", nargs=2, type=float, help=program.r_help)
    return parser


def parse_url(url: str) -> str:
    domain = urllib.parse.urlparse(url).netloc
    if domain in VALID_URLS:
        return url
    else:
        raise DownloaderExceptionUrlWithoutCoverage()


def parse_chapter_range(chapter_range: list[int] | None) -> list[int] | None:
    if not chapter_range:
        return None
    valid_pattern = chapter_range[1] > chapter_range[0]
    if not valid_pattern:
        raise DownloaderExceptionInvalidPattern()
    return chapter_range
