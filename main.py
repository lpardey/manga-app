# Standard Library
from parser.parser import get_parser, parse_chapter_range, parse_url

# Dependencies
import requests
from bs4 import BeautifulSoup

# From apps
from logic.app import Downloader


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    url, domain = parse_url(args.url)
    directory_path = args.path
    chapters = args.chapter
    chapter_range = parse_chapter_range(args.chapter_range)
    html_doc = requests.get(url).text
    web_data = BeautifulSoup(html_doc, "html.parser")
    downloader = Downloader.get_downloader(domain, web_data, directory_path, chapters, chapter_range)
    downloader.mangadanga()


if __name__ == "__main__":
    main()
