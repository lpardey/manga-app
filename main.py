from bs4 import BeautifulSoup
import requests
from logic.app import Downloader, Manganato
from parser.parser import get_parser, parse_url, parse_chapter_range


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    url = parse_url(args.url)
    chapters = args.chapter
    chapter_range = parse_chapter_range(args.chapter_range)
    html_doc = requests.get(url).text
    web_data = BeautifulSoup(html_doc, "html.parser")
    downloader = Manganato(web_data, chapters, chapter_range)
    downloader.mangadanga()


if __name__ == "__main__":
    main()
