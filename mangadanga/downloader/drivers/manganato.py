from bs4 import BeautifulSoup
from pathlib import PurePath

from .. import utils

from ..models import ChapterIndex
from ..base import Downloader


class Manganato(Downloader):
    URL = "https://manganato.com/"
    DOMAINS = {"manganato.com", "chapmanganato.com"}
    EXTRA_HEADERS = {"Referer": f"{URL}"}

    def get_title(self, data: BeautifulSoup) -> str:
        title_div = data.find(class_="story-info-right")
        title = title_div.find("h1").string
        return title

    def get_all_chapters_to_url(self, data: BeautifulSoup) -> dict[ChapterIndex, str]:
        chapter_content = data.find(class_="panel-story-chapter-list").find_all("a")
        chapter_content.reverse()
        chapter_number_to_url = {
            ChapterIndex(PurePath(data["href"]).name.replace("chapter-", "")): data["href"] for data in chapter_content
        }
        return chapter_number_to_url

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="panel-chapter-info-top").find("h1").string
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_filename = f"{index}_{formatted_chapter_title}.zip"
        return chapter_filename

    async def get_images_src(self, data: BeautifulSoup) -> list[str]:
        images = data.find(class_="container-chapter-reader").find_all("img")
        images_src = [img["src"] for img in images]
        return images_src
