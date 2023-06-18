from argparse import ArgumentParser
from pydantic import BaseModel
from urllib.parse import urlparse
from logic.app import DownloaderExceptionNoChapters, DownloaderExceptionUrlWithoutCoverage


VALID_URLS = {"chapmanganato.com"}


class MangaDanga(BaseModel):
    name: str = "MangaDanga"
    description: str = "Download your favorite graphic novels. Enter the url where the novel is, a directory named after the novel will be created and zip files will be created for each chapter of the novel with its corresponding images. By default, the downloaded files will be stored where you execute the program. Enjoy!"
    usage: str = "%(prog)s [options]"
    epilog: str = "Chachi"
    chapter_help: str = (
        "Display the chapter or group of chapters required to download. Use '-' to denote a group e.g., 1-5"
    )


def get_parser() -> ArgumentParser:
    program = MangaDanga()
    parser = ArgumentParser(
        prog=program.name,
        usage=program.usage,
        description=program.description,
        epilog=program.epilog,
    )
    parser.add_argument("url", help="Display a url of the graphic novel to download")
    parser.add_argument("-c", "--chapters", nargs="*", help=program.chapter_help)
    parser.add_argument("-t", "--threads", default=0, type=int, help="Display a number of threads to use")
    return parser


def parse_url(url: str) -> str | None:
    domain = urlparse(url).netloc
    if domain in VALID_URLS:
        return url
    else:
        raise DownloaderExceptionUrlWithoutCoverage()


def parse_chapters(chapters: list[str] | None) -> list[str, list[str]] | None:
    if not chapters:
        if isinstance(chapters, list):
            raise DownloaderExceptionNoChapters()
        else:
            return None
    for i in range(len(chapters)):
        if not chapters[i].isnumeric():
            chapters[i] = chapters[i].split("-")
    return chapters
