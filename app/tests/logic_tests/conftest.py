import pytest
from bs4 import BeautifulSoup
import requests


@pytest.fixture()
def web_data_main_page() -> BeautifulSoup:
    html_doc = requests.get("https://chapmanganato.com/manga-uh955964").text
    web_data_main_page = BeautifulSoup(html_doc, "lxml")
    return web_data_main_page
