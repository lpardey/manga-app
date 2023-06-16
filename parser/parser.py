from argparse import ArgumentParser, Namespace
from pydantic import BaseModel
from urllib.parse import urlparse

VALID_URLS = {"chapmanganato.com"}


class MangaDanga(BaseModel):
    name: str = "MangaDanga"
    description: str = "Download your favorite graphic novels. Enter the url where the novel is, a directory named after the novel will be created and zip files will be created for each chapter of the novel with its corresponding images. By default, the downloaded files will be stored where you execute the program. Enjoy!"


def get_parser() -> ArgumentParser:
    program = MangaDanga()
    parser = ArgumentParser(prog=program.name, description=program.description)
    parser.add_argument("url", help="Display a url of the graphic novel to download")
    parser.add_argument("-t", "--threads", type=int, default=0, help="Display a number of threads to use")
    return parser


def parse_url(parser: ArgumentParser) -> str | None:
    url = parser.parse_args().url
    domain = urlparse(url).netloc
    return url if domain in VALID_URLS else None
