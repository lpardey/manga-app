from bs4 import BeautifulSoup

from app.logic.schemas import Chapter, Image


def test_create_directory(web_data: BeautifulSoup) -> None:
    assert True


def test_get_chapters(web_data: BeautifulSoup) -> list[Chapter]:
    assert True


def test_get_images(web_data: BeautifulSoup) -> list[Image]:
    """Get a list of images"""
    pass


def test_create_zip_file(chapters: list[Chapter]) -> None:
    """Generate a zip file inside a directory for every chapter of the manga"""
    assert True
