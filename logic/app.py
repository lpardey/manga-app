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
    domain: str | list[str]
    extra_headers: dict[str, str]

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

    def in_chapters(self, chapter: tuple[float, str]) -> bool:
        """Lambda to filter the chapters to download"""
        return chapter[0] in self.chapters

    def in_chapter_range(self, chapter: tuple[float, str]) -> bool:
        """Lambda to filter the chapters to download"""
        return self.chapter_range[0] <= chapter[0] <= self.chapter_range[1]

    def add_image(self, zipfile: ZipFile, image_index: int, image_url: str) -> None:
        """Adds image to a zip file"""
        image_data = requests.get(image_url, headers=self.get_headers()).content
        image_basename = os.path.basename(image_url)
        formatted_image_name = utils.format_name(image_basename)
        image_filename = f"{image_index:04}_{formatted_image_name}"
        zipfile.writestr(image_filename, image_data)

    def download_chapter(self, directory_path: str, index: int, chapter_url: str) -> None:
        """Gets chapter data, creates a zip file by its name, and downloads and stores its images to the zip file"""
        data = BeautifulSoup(requests.get(chapter_url, headers=self.get_headers()).text, "html.parser")
        chapter_filename = self.get_chapter_filename(index, data)
        chapter_path = os.path.join(directory_path, chapter_filename)
        images_url = self.get_images_src(data)
        with ZipFile(chapter_path, "w") as zipf:
            for image_index, image_url in enumerate(images_url):
                self.add_image(zipf, image_index, image_url)

    def mangadanga(self) -> None:
        """Creates a directory and downloads chapters, in other words: MangaDanga!"""
        chapter_number_to_url = self.get_chapter_number_to_url()
        directory_path = self.create_directory()
        for index, url in chapter_number_to_url.items():
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
        if any(True for downloader_domain in Manganato.domain if domain == downloader_domain):
            return Manganato(web_data, directory_path, chapters, chapter_range)
        elif domain == Mangatown.domain:
            return Mangatown(web_data, directory_path, chapters, chapter_range)
        elif domain == Mangadoom.domain:
            return Mangadoom(web_data, directory_path, chapters, chapter_range)
        else:
            raise utils.DownloaderExceptionUnexpected("Couldn't get a downloader")

    @abstractmethod
    def get_title(self) -> str:
        """Scrapes a title"""
        pass

    @abstractmethod
    def get_chapter_number_to_url(self) -> dict[float, str]:
        """Scrapes chapters urls. Returns a list of chapters urls by reading order (first, second, etc.)"""
        pass

    @abstractmethod
    def get_chapter_filename(self) -> str:
        """Scrapes chapter name. Returns its path with '.zip' extension"""
        pass

    @abstractmethod
    def get_images_src(self) -> list[str]:
        """Scrapes images urls"""
        pass


class Manganato(Downloader):
    url = "https://manganato.com/"
    domain = ["manganato.com", "chapmanganato.com"]
    extra_headers = {"Referer": f"{url}"}

    def get_title(self) -> str:
        title_div = self.web_data.find(class_="story-info-right")
        title = title_div.find("h1").string
        return title

    def get_chapter_number_to_url(self) -> dict[float, str]:
        chapter_content = self.web_data.find(class_="panel-story-chapter-list").find_all("a")
        chapter_content.reverse()
        chapter_number_to_url = {
            float(PurePath(data["href"]).name.replace("chapter-", "")): data["href"] for data in chapter_content
        }
        if self.chapters:
            chapter_number_to_url = dict(filter(self.in_chapters, chapter_number_to_url.items()))
        if self.chapter_range:
            chapter_number_to_url = dict(filter(self.in_chapter_range, chapter_number_to_url.items()))
        return chapter_number_to_url

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="panel-chapter-info-top").find("h1").string
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_file = f"{index}_{formatted_chapter_title}.zip"
        chapter_path = os.path.join(self.directory_path, chapter_file)
        return chapter_path

    def get_images_src(self, data: BeautifulSoup) -> list[str]:
        images = data.find(class_="container-chapter-reader").find_all("img")
        images_src = [img["src"] for img in images]
        return images_src


class Mangatown(Downloader):
    url = "https://www.mangatown.com/"
    domain = "www.mangatown.com"
    extra_headers = {"Referer": f"{url}"}

    def get_title(self) -> str:
        title = self.web_data.find(class_="title-top").string
        return title

    def get_chapter_number_to_url(self) -> dict[float, str]:
        chapter_content = self.web_data.find(class_="chapter_list").find_all("a")
        chapter_content.reverse()
        chapter_number_to_url = {
            float(PurePath(data["href"]).name.replace("c", "").lstrip("0")): f"{self.url}" + data["href"]
            for data in chapter_content
        }
        if self.chapters:
            chapter_number_to_url = dict(filter(self.in_chapters, chapter_number_to_url.items()))
        if self.chapter_range:
            chapter_number_to_url = dict(filter(self.in_chapter_range, chapter_number_to_url.items()))
        return chapter_number_to_url

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="title").find("h1").string
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_file = f"{index}_{formatted_chapter_title}.zip"
        chapter_path = os.path.join(self.directory_path, chapter_file)
        return chapter_path

    def get_images_src(self, data: BeautifulSoup) -> list[str]:
        try:
            data.find(class_="page_select").find("option", string="Featured").extract()  # Unnecessary Ad element
            number_of_imgs = len(data.find(class_="page_select").find_all("option"))
            first_img_src = "https:" + data.find(class_="read_img").find("img")["src"]
            src_numbers_suffix = utils.get_src_numbers_suffix(first_img_src)
            images_src = [first_img_src]
            for i in range(1, number_of_imgs):
                new_suffix = str(int(src_numbers_suffix) + i).zfill(len(src_numbers_suffix))
                images_src.append(first_img_src.replace(src_numbers_suffix, new_suffix))
        except:
            images_src = self.get_images_src_exhaustive_search(data)
        return images_src

    def get_images_src_exhaustive_search(self, data: BeautifulSoup) -> list[str]:
        data.find(class_="page_select").find("option", string="Featured").extract()  # Unnecessary Ad element
        data_options = data.find(class_="page_select").find_all("option")
        html_doc = [self.url + url["value"] for url in data_options]
        images_src = [
            "https:" + BeautifulSoup(requests.get(url).text, "html.parser").find(class_="read_img").find("img")["src"]
            for url in html_doc
        ]
        return images_src


class Mangadoom(Downloader):
    url = "https://www.mngdoom.com/"
    domain = "www.mngdoom.com"
    extra_headers = {"Referer": f"{url}"}

    def get_title(self) -> str:
        title_div = self.web_data.find(class_="widget-heading")
        title = title_div.string
        return title

    def get_chapter_number_to_url(self) -> dict[float, str]:
        chapter_content = self.web_data.find(class_="chapter-list").find_all("a")
        chapter_content.reverse()
        chapter_number_to_url = {float(PurePath(data["href"]).name): data["href"] for data in chapter_content}
        if self.chapters:
            chapter_number_to_url = dict(filter(self.in_chapters, chapter_number_to_url.items()))
        if self.chapter_range:
            chapter_number_to_url = dict(filter(self.in_chapter_range, chapter_number_to_url.items()))
        return chapter_number_to_url

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="col-md-8 col-xs-12").text.strip()
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_file = f"{index}_{formatted_chapter_title}.zip"
        chapter_path = os.path.join(self.directory_path, chapter_file)
        return chapter_path

    def get_images_src(self, data: BeautifulSoup) -> list[str]:
        try:
            number_of_imgs = len(data.find(class_="selectPage pull-right chapter-page1").find_all("option"))
            first_img_src = data.find(class_="img-responsive")["src"]
            src_numbers_suffix = utils.get_src_numbers_suffix(first_img_src)
            images_src = [first_img_src]
            for i in range(1, number_of_imgs):
                new_suffix = str(int(src_numbers_suffix) + i).zfill(len(src_numbers_suffix))
                images_src.append(first_img_src.replace(src_numbers_suffix, new_suffix))
        except:
            images_src = self.get_images_src_exhaustive_search(data)
        return images_src

    def get_images_src_exhaustive_search(self, data: BeautifulSoup) -> list[str]:
        data_options = data.find(class_="selectPage pull-right chapter-page1").find_all("option")
        html_doc = [url["value"] for url in data_options]
        images_src = [
            BeautifulSoup(requests.get(url).text, "html.parser").find(class_="img-responsive")["src"]
            for url in html_doc
        ]
        return images_src
