from bs4 import BeautifulSoup

from .. import utils

from ..models import ChapterIndex
from ..base import Downloader

from ..models import ChapterIndex


class Mangadoom(Downloader):
    URL = "https://www.mngdoom.com/"
    DOMAINS = {"www.mngdoom.com"}
    EXTRA_HEADERS = {"Referer": f"{URL}"}

    def get_title(self, data: BeautifulSoup) -> str:
        title_div = data.find(class_="widget-heading")
        title = title_div.string
        return title

    def get_all_chapters_to_url(self, data: BeautifulSoup) -> dict[ChapterIndex, str]:
        chapter_content = data.find(class_="chapter-list").find_all("a")
        chapter_content.reverse()
        separators = []
        chapter_number_to_url = {
            ChapterIndex(self.get_chapter_index(data, separators)): data["href"] for data in chapter_content
        }
        return chapter_number_to_url

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="col-md-8 col-xs-12").text.strip()
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_file = f"{index}_{formatted_chapter_title}.zip"
        return chapter_file

    async def get_images_src(self, data: BeautifulSoup) -> list[str]:
        data_options = data.find(class_="selectPage pull-right chapter-page1").find_all("option")
        chapter_data = [await self.scrape_url(url["value"]) for url in data_options]
        images_src = [data.find(class_="img-responsive")["src"] for data in chapter_data]
        return images_src
