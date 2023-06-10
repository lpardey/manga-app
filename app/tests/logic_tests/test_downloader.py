import pytest
from unittest import mock
from bs4 import BeautifulSoup
from app.logic.app import Downloader


def test_create_directory_success(web_data_main_page: BeautifulSoup):
    downloader = Downloader(web_data=web_data_main_page)
    dir_name = "Fullmetal Alchemist"
    response = downloader.create_directory()
    assert response == None


# def create_directory(self) -> None:
#     """Generate a directory named after the manga"""
#     scraped_data = self.web_data.find("title")
#     if scraped_data is None:  # TODO: Ask user for a title name to create the dir instead of raising exception
#         raise DownloaderExceptionMissingTitle()

#     try:
#         dir_name = scraped_data.name
#         path = os.path.join(self.dir_path, dir_name)
#         os.mkdir(path)
#     except DownloaderException as e:
#         raise DownloaderExceptionUnexpected(str(e))
