# Standard Library
from abc import ABC, abstractmethod
import os
import shutil

# Dependencies
from bs4 import BeautifulSoup

from app.logic.schemas import Chapter, Image


class DownloaderException(Exception):
    pass


class DownloaderExceptionMissingTitle(DownloaderException):
    def __init__(self, message: str = "Couldn't retrieve the Manga's title from the website") -> None:
        self.message = message
        super().__init__(self.message)


class DownloaderExceptionUnexpected(DownloaderException):
    pass


DESKTOP_PATH = os.path.expanduser("~/Desktop")  # Supports Unix or Windows (after 7)


class Downloader(ABC):
    def __init__(self, web_data: BeautifulSoup, desktop_path: str = DESKTOP_PATH) -> None:
        super().__init__()
        self.web_data = web_data
        self.desktop_path = desktop_path

    @abstractmethod
    def get_directory_name(self) -> str:
        """Get the directory name and return it as str"""
        pass

    @abstractmethod
    def create_directory(self) -> str:
        """Generate a directory named after the manga's title and returns its path"""
        pass

    def create_chapter_obj(self, number: int, name: str, images: list[Image]) -> Chapter:
        return Chapter(number, name, images)

    @abstractmethod
    def get_chapters(self) -> list[Chapter]:
        """Pull data out of website and return a list of Chapter objects."""
        pass

    @abstractmethod
    def get_images(self) -> list[Image]:
        """Get a list of images"""
        pass

    @abstractmethod
    def create_zip_file(path: str, chapters: list[Chapter]) -> None:
        """Generate a zip file inside the directory for every chapter of the manga"""
        # Create zip file
        # Add chapter to zip file
        pass


class Manganato(Downloader):
    def get_directory_name(self) -> str:
        scraped_data = self.web_data.find("title")
        if scraped_data is None:  # TODO: Ask user for a title name to create the dir instead of raising exception
            raise DownloaderExceptionMissingTitle()
        dir_name = scraped_data.string.removesuffix("Manga Online Free - Manganato").strip()
        return dir_name

    def create_directory(self) -> str:
        dir_name = self.get_directory_name()
        path = os.path.join(self.desktop_path, dir_name)
        path_exists = os.path.exists(path)
        try:
            if path_exists:  # TODO: Ask user if he wants to overwrite or not. Handle 'FileExistsError'.
                shutil.rmtree(path)  # Delete existing directory tree
            os.mkdir(path)  # TODO: Path is not equal to /home/lpardey/Desktop and is giving an error
            return path  # Param for the main function.
        except DownloaderException as e:
            raise DownloaderExceptionUnexpected(str(e))

    def get_chapters(self) -> list[Chapter]:
        """Pull data out of website and return a list of Chapter objects."""
        scraped_data = self.web_data.find_all("a", class_="chapter-name text-nowrap").reverse()
        chapter_obj = self.create_chapter_obj()  # Map this func with the scraped_data
        pass

    def get_images(self) -> list[Image]:
        """Get a list of images"""
        scraped_data = self.web_data.select_one("div.container-chapter-reader").findChildren("img")
        images = [Image(number=index, source=data["src"]) for index, data in enumerate(scraped_data, start=1)]
        return images

    def create_zip_file(path: str, chapters: list[Chapter]) -> None:
        pass
