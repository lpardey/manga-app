# Standard Library
from abc import ABC, abstractmethod
import os

# Dependencies
from bs4 import BeautifulSoup

from app.logic.schemas import Chapter, Image


class DownloaderException(Exception):
    pass


class DownloaderExceptionMissingTitle(DownloaderException):
    def __init__(
        self, message: str = "Couldn't retrieve the Manga's title from the website to create the directory file"
    ) -> None:
        self.message = message
        super().__init__(self.message)


class DownloaderExceptionUnexpected(DownloaderException):
    pass


DESKTOP_PATH = os.path.expanduser("~/Desktop")  # Supports Unix or Windows (after 7)


class Downloader(ABC):
    @abstractmethod
    def __init__(self, web_data: BeautifulSoup, dir_path: str = DESKTOP_PATH) -> None:
        super().__init__()
        self.web_data = web_data
        self.dir_path = dir_path

    @abstractmethod
    def create_directory(self) -> None:
        """Generate a directory named after the manga's title"""
        pass

    @abstractmethod
    def get_chapters(self) -> list[Chapter]:
        """Pull data out of website and return a list of Chapter objects."""
        pass

    @abstractmethod
    def get_images(self) -> list[Image]:
        """Get a list of images"""
        pass

    @staticmethod
    def create_zip_file(chapters: list[Chapter]) -> None:
        """Generate a zip file inside the directory for every chapter of the manga"""
        # Create zip file
        # Add chapter to zip file
        pass


class Manganato(Downloader):
    def __init__(self, web_data: BeautifulSoup, dir_path: str) -> None:
        super().__init__()
        self.web_data = web_data
        self.dir_path = dir_path

    def create_directory(self) -> None:
        """Generate a directory named after the manga"""
        scraped_data = self.web_data.find("title")
        dir_name = scraped_data.name
        if dir_name is None:  # TODO: Ask user for a title name to create the dir instead of raising exception
            raise DownloaderExceptionMissingTitle()

        path = os.path.join(self.dir_path, dir_name)
        try:
            os.mkdir(path)
        except DownloaderException as e:
            raise DownloaderExceptionUnexpected(str(e))

    @abstractmethod
    def get_chapters(self) -> list[Chapter]:
        """Pull data out of website and return a list of Chapter objects."""
        pass

    @abstractmethod
    def get_images(self) -> list[Image]:
        """Get a list of images"""
        pass
