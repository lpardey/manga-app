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
    def create_directory(self) -> None:
        """Generate a directory named after the manga"""
        scraped_data = self.web_data.find("title")
        if scraped_data is None:  # TODO: Ask user for a title name to create the dir instead of raising exception
            raise DownloaderExceptionMissingTitle()

        try:
            dir_name = scraped_data.string.removesuffix("Manga Online Free - Manganato").strip()
            path = os.path.join(self.desktop_path, dir_name)
            if os.path.exists(path):
                # TODO: Ask user if he wants to overwrite or not.Handle 'FileExistsError'.
                shutil.rmtree(path)  # overwrite
            os.mkdir(path)  # Path is not equal to /home/lpardey/Desktop and is iving an error
        except DownloaderException as e:
            raise DownloaderExceptionUnexpected(str(e))

    def get_chapters(self) -> list[Chapter]:
        """Pull data out of website and return a list of Chapter objects."""
        pass

    def get_images(self) -> list[Image]:
        """Get a list of images"""
        pass
