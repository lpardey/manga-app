# Standard Library
import logging
import os
from abc import ABC, abstractmethod
from pathlib import PurePath
from zipfile import ZipFile

# Dependencies
import requests
from bs4 import BeautifulSoup

# Local imports
from . import utils

logger = logging.getLogger(__name__)


class Downloader(ABC):
    url: str
    domain: str
    extra_headers: str

    def __init__(
        self,
        web_data: BeautifulSoup,
        directory_path: str,
        chapters: list[int] | None = None,
        chapter_range: list[int] | None = None,
    ) -> None:
        super().__init__()
        self.web_data = web_data
        self.chapters = chapters
        self.chapter_range = chapter_range
        self.directory_path = directory_path

    def get_directory_name(self) -> str:
        """Scrapes a title from website and returns it in an suitable format"""
        title = self.get_title()
        dir_name = utils.format_name(title)
        return dir_name

    def create_directory(self) -> str:
        """Creates a directory on the path specified (default path: '.'). Returns directory path"""
        dir_name = self.get_directory_name()
        path = os.path.join(self.directory_path, dir_name)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def get_headers(self) -> dict[str, str]:
        basic_headers = dict()
        basic_headers.update(self.extra_headers)
        return basic_headers

    def add_image(self, zipfile: ZipFile, image_index: int, image_url: str) -> None:
        """Adds an image to a zip file"""
        image_data = self.download_image(image_url)
        image_basename = os.path.basename(image_url)
        formatted_image_name = utils.format_name(image_basename)
        image_filename = f"{image_index:04}_{formatted_image_name}"
        zipfile.writestr(image_filename, image_data)

    def download_chapter(self, directory_path: str, index: int, chapter_url: str) -> None:
        """Gets chapter data, creates a zip file by its name, and downloads and stores its images to the zip file"""
        data = BeautifulSoup(requests.get(chapter_url, headers=self.get_headers()).text, "html.parser")
        chapter_filename = self.get_chapter_filename(index, data)
        chapter_path = os.path.join(directory_path, chapter_filename)
        images_url = self.get_images_urls(data)
        with ZipFile(chapter_path, "w") as zipf:
            for image_index, image_url in enumerate(images_url):
                self.add_image(zipf, image_index, image_url)

    def mangadanga(self) -> None:
        """Creates a directory and downloads all chapters, in other words: MangaDanga!"""
        chapter_numbers_to_url = self.get_chapter_numbers_to_urls()
        directory_path = self.create_directory()
        for index, url in chapter_numbers_to_url.items():
            self.download_chapter(directory_path, index, url)

    @classmethod
    def get_downloader(
        cls,
        domain: str,
        web_data: BeautifulSoup,
        directory_path: str,
        chapters: list[int] | None,
        chapter_range: list[int] | None,
    ) -> "Downloader":
        match domain:
            case Manganato.domain:
                return Manganato(web_data, directory_path, chapters, chapter_range)
            case Mangatown.domain:
                return Mangatown(web_data, directory_path, chapters, chapter_range)
            case _:
                raise utils.DownloaderExceptionUnexpected()

    @abstractmethod
    def get_title(self) -> str:
        """Scrapes a title"""
        pass

    @abstractmethod
    def get_chapter_numbers_to_urls(self) -> dict[float, str]:
        """Scrapes chapters urls. Returns a list of chapters urls by reading order (first, second, etc.)"""
        pass

    @abstractmethod
    def get_chapter_filename(self) -> str:
        """Scrapes chapter name. Returns its path with '.zip' extension"""
        pass

    @abstractmethod
    def get_images_urls(self) -> list[str]:
        """Scrapes images urls"""
        pass

    @abstractmethod
    def download_image(self) -> None:
        """Sends a get request and returns its content response in bytes"""
        pass


class Manganato(Downloader):
    url = "https://manganato.com/"
    domain = "chapmanganato.com"
    extra_headers = {"Referer": "https://chapmanganato.com/"}

    def get_title(self) -> str:
        title_div = self.web_data.find(class_="story-info-right")
        title = title_div.find("h1").string
        return title

    def get_chapter_numbers_to_urls(self) -> dict[float, str]:
        chapter_links = self.web_data.find_all("a", class_="chapter-name")
        chapter_links.reverse()
        chapter_numbers_to_urls = {
            float(PurePath(data["href"]).name.replace("chapter-", "")): data["href"] for data in chapter_links
        }
        if self.chapters:
            chapter_numbers_to_urls = dict(filter(lambda i: i[0] in self.chapters, chapter_numbers_to_urls.items()))

        if self.chapter_range:
            chapter_numbers_to_urls = dict(
                filter(
                    lambda i: self.chapter_range[0] <= i[0] <= self.chapter_range[1], chapter_numbers_to_urls.items()
                )
            )
        return chapter_numbers_to_urls

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="panel-chapter-info-top").find("h1").string
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_file = f"{index}_{formatted_chapter_title}.zip"
        chapter_path = os.path.join(self.directory_path, chapter_file)
        return chapter_path

    def get_images_urls(self, data: BeautifulSoup) -> list[str]:
        images = data.find(class_="container-chapter-reader").find_all("img")
        images_src = [img["src"] for img in images]
        return images_src

    def download_image(self, image_url: str) -> bytes:
        response = requests.get(image_url, headers=self.get_headers())
        return response.content


class Mangatown(Downloader):
    url = "https://www.mangatown.com"
    domain = "www.mangatown.com"
    extra_headers = {"Referer": "https://www.mangatown.com/"}

    def get_title(self) -> str:
        title = self.web_data.find(class_="title-top").string
        return title

    def get_chapter_numbers_to_urls(self) -> dict[float, str]:
        partial_chapter_links = self.web_data.find(class_="chapter_list").find_all("a")
        partial_chapter_links.reverse()
        chapter_numbers_to_urls = {
            float(PurePath(data["href"]).name.replace("c", "").lstrip("0")): f"{self.url}" + data["href"]
            for data in partial_chapter_links
        }
        if self.chapters:
            chapter_numbers_to_urls = dict(filter(lambda i: i[0] in self.chapters, chapter_numbers_to_urls.items()))

        if self.chapter_range:
            chapter_numbers_to_urls = dict(
                filter(
                    lambda i: self.chapter_range[0] <= i[0] <= self.chapter_range[1], chapter_numbers_to_urls.items()
                )
            )
        return chapter_numbers_to_urls

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="title").find("h1").string
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_file = f"{index}_{formatted_chapter_title}.zip"
        chapter_path = os.path.join(self.directory_path, chapter_file)
        return chapter_path

    def get_images_urls(self, data: BeautifulSoup) -> list[str]:
        data.find(class_="page_select").find("option", string="Featured").extract()  # Unnecessary Ad element
        options_tag = data.find(class_="page_select").find_all("option")
        img_html_url = [self.url + url["value"] for url in options_tag]
        images_src = [
            "https:" + BeautifulSoup(requests.get(url).text, "html.parser").find(class_="read_img").find("img")["src"]
            for url in img_html_url
        ]
        return images_src

    def download_image(self, image_url: str) -> bytes:
        response = requests.get(image_url, headers=self.get_headers())
        return response.content


# basic_headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
#     "Accept": "image/avif,image/webp,*/*",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Connection": "keep-alive",
#     "Referer": "https://chapmanganato.com/",
#     "Sec-Fetch-Dest": "image",
#     "Sec-Fetch-Mode": "no-cors",
#     "Sec-Fetch-Site": "cross-site",
#     "Pragma": "no-cache",
#     "Cache-Control": "no-cache",
#     "TE": "trailers",
# }
