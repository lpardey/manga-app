from pathlib import PurePath
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
        chapter_number_to_url = {
            ChapterIndex(PurePath(data["href"]).name.replace("c", "").lstrip("0")): f"{self.URL}" + data["href"]
            for data in chapter_content
        }
        return chapter_number_to_url

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="title").find("h1").string
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_filename = f"{index}_{formatted_chapter_title}.zip"
        return chapter_filename

    async def get_images_src(self, data: BeautifulSoup) -> list[str]:
        data.find(class_="page_select").find("option", string="Featured").extract()  # Unnecessary Ad element
        try:
            # Not downloading the images using this algorithm. Maybe async issues.
            number_of_imgs = len(data.find(class_="page_select").find_all("option"))
            first_img_src: str = "https:" + data.find(class_="read_img").find("img")["src"]
            src_numbers_suffix = self.get_src_numbers_suffix(first_img_src)
            images_src = [first_img_src]
            for i in range(1, number_of_imgs):
                new_suffix = str(int(src_numbers_suffix) + i).zfill(len(src_numbers_suffix))
                images_src.append(first_img_src.replace(src_numbers_suffix, new_suffix))
        except:
            # Works but its slow
            images_src = await self.get_images_src_exhaustive_search(data)
        return images_src

    async def get_images_src_exhaustive_search(self, data: BeautifulSoup) -> list[str]:
        data_options = data.find(class_="page_select").find_all("option")
        chapter_data = [await self.scrap_main_url(self.URL + url["value"]) for url in data_options]
        images_src = ["https:" + data.find(class_="read_img").find("img")["src"] for data in chapter_data]
        return images_src
