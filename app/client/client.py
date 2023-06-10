from bs4 import BeautifulSoup
import requests


class DownloaderClient:
    def get_html_doc(url: str) -> str:
        response = requests.get(url)
        html_doc = response.text
        return html_doc

    def get_web_data(html_doc: str) -> BeautifulSoup:
        return BeautifulSoup(html_doc, "lxml")
