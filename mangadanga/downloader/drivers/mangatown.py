from bs4 import BeautifulSoup

from .. import utils
from ..models import ChapterIndex
from ..base import Downloader


class Mangatown(Downloader):
    URL = "https://www.mangatown.com/"
    DOMAINS = {"www.mangatown.com"}
    EXTRA_HEADERS = {"Referer": f"{URL}"}

    def get_title(self, data: BeautifulSoup) -> str:
        title = data.find(class_="title-top").string
        return title

    def get_all_chapters_to_url(self, data: BeautifulSoup) -> dict[ChapterIndex, str]:
        chapter_content = data.find(class_="chapter_list").find_all("a")
        chapter_content.reverse()
        separators = ["c"]
        chapter_number_to_url = {
            ChapterIndex(self.get_chapter_index(data, separators)): f"{self.URL}" + data["href"]
            for data in chapter_content
        }
        return chapter_number_to_url

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="title").find("h1").string
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_filename = f"{index}_{formatted_chapter_title}.zip"
        return chapter_filename

    async def get_images_src(self, data: BeautifulSoup) -> list[str]:
        data.find(class_="page_select").find("option", string="Featured").extract()
        data_options = data.find(class_="page_select").find_all("option")
        chapter_data = [await self.scrape_url(self.URL + url["value"]) for url in data_options]
        images_src = ["https:" + data.find(class_="read_img").find("img")["src"] for data in chapter_data]
        return images_src
