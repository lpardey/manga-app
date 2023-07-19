from bs4 import BeautifulSoup
import logging
import os
from pathlib import PurePath

from .. import utils
from ..models import ChapterIndex
from ..base import Downloader


logger = logging.getLogger("MangatownDownloader")


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

    def extrapolate_image_url(self, base_url: str, page_index: int, padding: int) -> str:
        # recibimos esto
        # "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_01.jpg",

        # esperamos devolver
        # "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_14.jpg",
        new_suffix = f"{page_index:0{padding}d}"
        path, name = os.path.split(base_url)
        base_name, extension = os.path.splitext(name)
        base_name_sub_strings = base_name.split("_")
        base_name_sub_strings[-1] = new_suffix
        new_name = "_".join(base_name_sub_strings) + extension
        new_url = f"{path}/{new_name}"
        return new_url

    async def get_images_src(self, data: BeautifulSoup) -> list[str]:
        data.find(class_="page_select").find("option", string="Featured").extract()  # Unnecessary Ad element
        # Not downloading the images using this algorithm. Maybe async issues.
        # number_of_imgs = len(data.find(class_="page_select").find_all("option"))
        # first_img_src: str = "https:" + data.find(class_="read_img").find("img")["src"]
        # src_numbers_suffix = self.get_src_numbers_suffix(first_img_src)

        # base_index = int(src_numbers_suffix)
        # padding = len(src_numbers_suffix)
        # images_src = [
        #     self.extrapolate_image_url(first_img_src, i, padding) for i in range(base_index, number_of_imgs + 1)
        # ]

        # Works but its slow
        images_src = await self.get_images_src_exhaustive_search(data)

        # if images_src != images_src_safe:
        #     # print differences in images_src and images_src_safe
        #     logger.error(f"images_src and images_src_safe are different. {images_src} != {images_src_safe}")
        #     logger.error(set(images_src) - set(images_src_safe))
        #     logger.error(set(images_src_safe) - set(images_src))
        #     raise Exception("images_src and images_src_safe are different")
        return images_src

    # async def get_images_src_old(self, data: BeautifulSoup) -> list[str]:
    #     data.find(class_="page_select").find("option", string="Featured").extract()  # Unnecessary Ad element
    #     try:
    #         # Not downloading the images using this algorithm. Maybe async issues.
    #         number_of_imgs = len(data.find(class_="page_select").find_all("option"))
    #         first_img_src: str = "https:" + data.find(class_="read_img").find("img")["src"]
    #         src_numbers_suffix = self.get_src_numbers_suffix(first_img_src)
    #         images_src = [first_img_src]
    #         for i in range(1, number_of_imgs):
    #             new_suffix = str(int(src_numbers_suffix) + i).zfill(len(src_numbers_suffix))
    #             images_src.append(first_img_src.replace(src_numbers_suffix, new_suffix))
    #     except:
    #         # Works but its slow
    #         images_src = await self.get_images_src_exhaustive_search(data)
    #     return images_src

    async def get_images_src_exhaustive_search(self, data: BeautifulSoup) -> list[str]:
        data_options = data.find(class_="page_select").find_all("option")
        chapter_data = [await self.scrape_url(self.URL + url["value"]) for url in data_options]
        images_src = ["https:" + data.find(class_="read_img").find("img")["src"] for data in chapter_data]
        return images_src
