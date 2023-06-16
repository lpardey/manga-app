from bs4 import BeautifulSoup
import requests
from logic.app import DownloaderExceptionUrlWithoutCoverage, Manganato
from parser.parser import get_parser, parse_url


def main() -> None:
    parser = get_parser()
    url = parse_url(parser)
    if not url:
        raise DownloaderExceptionUrlWithoutCoverage()
    html_doc = requests.get(url).text
    web_data = BeautifulSoup(html_doc, "html.parser")
    downloader = Manganato(web_data)
    downloader.mangadanga()


if __name__ == "__main__":
    main()
