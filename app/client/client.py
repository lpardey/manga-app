from bs4 import BeautifulSoup
import requests


class DownloaderClient:
    def get_data(url: str) -> requests.Response:
        response = requests.get(url)
        return response

    def get_web_data(html_doc: str) -> BeautifulSoup:
        return BeautifulSoup(html_doc, "lxml")
