from bs4 import BeautifulSoup

from app.logic.schemas import Chapter, Image


def test_create_directory(web_data: BeautifulSoup) -> None:
    """Generate a directory named after the manga's title"""
    assert True


def test_get_chapters(web_data: BeautifulSoup) -> list[Chapter]:
    """Pull data out of website and return a list of Chapter objects."""
    assert True


def test_get_images(web_data: BeautifulSoup) -> list[Image]:
    """Get a list of images"""
    assert True


def test_create_zip_file(chapters: list[Chapter]) -> None:
    """Generate a zip file inside the directory for every chapter of the manga"""
    # Create zip file
    # Add chapter to zip file
    assert True
