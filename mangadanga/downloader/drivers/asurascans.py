from bs4 import BeautifulSoup
from .. import utils
from ..models import ChapterIndex
from ..base import Downloader


class Asurascans(Downloader):
    URL = "https://asura.gg/"
    DOMAINS = {"www.asurascans.com", "asura.gg"}
    EXTRA_HEADERS = {"Referer": f"{URL}"}

    def get_title(self, data: BeautifulSoup) -> str:
        title = data.find(class_="entry-title").string
        return title

    def get_all_chapters_to_url(self, data: BeautifulSoup) -> dict[ChapterIndex, str]:
        chapter_content = data.find(class_="eplister").find_all("a")
        chapter_content.reverse()
        separators = ["chapter", "-"]
        chapter_number_to_url = {self.get_chapter_index(data, separators): data["href"] for data in chapter_content}
        return chapter_number_to_url

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="entry-title").string
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_filename = f"{index}_{formatted_chapter_title}.zip"
        return chapter_filename

    async def get_images_src(self, data: BeautifulSoup) -> list[str]:
        images = data.find(class_="rdminimal").find_all("img")
        images_src = [img["src"] for img in images]
        return images_src
