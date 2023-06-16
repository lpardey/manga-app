# Standard Library
import logging
import os
from abc import ABC, abstractmethod
from zipfile import ZipFile
import shutil

# Dependencies
import requests
from bs4 import BeautifulSoup

# Local imports
from . import utils

logger = logging.getLogger(__name__)


class DownloaderException(Exception):
    pass


class DownloaderExceptionMissingTitle(DownloaderException):
    def __init__(self, message: str = "Couldn't retrieve the graphic novel's title from the website") -> None:
        self.message = message
        super().__init__(self.message)


class DownloaderExceptionUrlWithoutCoverage(DownloaderException):
    def __init__(self, message: str = f"URL not registered in MangaDanga!") -> None:
        self.message = message
        super().__init__(self.message)


class DownloaderExceptionUnexpected(DownloaderException):
    pass


class Downloader(ABC):
    def __init__(
        self,
        web_data: BeautifulSoup,
        directory_path: str | None = None,
    ) -> None:
        super().__init__()
        self.web_data = web_data
        self.directory_path = directory_path if directory_path is not None else "."

    def get_directory_name(self) -> str:
        """Scrapes a title from website and returns it in an suitable format"""
        title = self.get_title()
        dir_name = utils.format_name(title)
        return dir_name

    def create_directory(self) -> str:
        """Creates a directory on the path specified (default path: '.'). Returns directory path"""
        dir_name = self.get_directory_name()
        path = os.path.join(self.directory_path, dir_name)
        os.makedirs(path, exist_ok=True)
        return path

    def get_headers(self) -> dict[str, str]:
        return dict()

    def add_image(self, zipfile: ZipFile, image_index: int, image_url: str) -> None:
        """Adds an image to a zip file"""
        image_data = self.download_image(image_url)
        image_basename = os.path.basename(image_url)
        formatted_image_name = utils.format_name(image_basename)
        image_filename = f"{image_index:04}_{formatted_image_name}"
        zipfile.writestr(image_filename, image_data)

    def download_chapter(self, directory_path: str, index: int, chapter_url: str) -> None:
        """Gets chapter data, creates a zip file by its name, and downloads and stores its images to the zip file"""
        data = BeautifulSoup(requests.get(chapter_url, headers=self.get_headers()).text, "html.parser")
        chapter_filename = self.get_chapter_filename(index, data)
        chapter_path = os.path.join(directory_path, chapter_filename)
        images_url = self.get_images_urls(data)
        with ZipFile(chapter_path, "w") as zipf:
            for image_index, image_url in enumerate(images_url):
                self.add_image(zipf, image_index, image_url)

    def mangadanga(self) -> None:
        """Creates a directory and downloads all chapters, in other words: MangaDanga!"""
        directory_path = self.create_directory()
        chapters_url = self.get_chapters_urls()
        for index, url in enumerate(chapters_url):
            self.download_chapter(directory_path, index, url)

    @abstractmethod
    def get_title(self) -> str:
        """Scrapes a title"""
        pass

    @abstractmethod
    def get_chapters_urls(self) -> list[str]:
        """Scrapes chapters urls. Returns a list of chapters urls by reading order (first, second, etc.)"""
        pass

    @abstractmethod
    def get_chapter_filename(self) -> str:
        """Scrapes chapter name. Returns its path with '.zip' extension"""
        pass

    @abstractmethod
    def get_images_urls(self) -> list[str]:
        """Scrapes images urls"""
        pass

    @abstractmethod
    def download_image(self) -> None:
        """Sends a get request and returns its content response in bytes"""
        pass

    # @abstractmethod
    # def get_images_data(self) -> BeautifulSoup:
    #     """Get images data and return it as a BeautifulSoup object"""
    #     pass

    # @abstractmethod
    # def get_images(self) -> list[Image]:
    #     """Parse images data and return a list of Image object"""
    #     pass

    # @abstractmethod
    # def create_zip_file(path: str, chapters: list[Chapter]) -> None:
    #     """Generate a zip file inside the directory for every chapter of the manga"""
    #     # Create zip file
    #     # Add chapter to zip file
    #     pass


class Manganato(Downloader):
    EXTRA_HEADERS = {"Referer": "https://chapmanganato.com/"}

    def get_title(self) -> str:
        title_div = self.web_data.find(class_="story-info-right")
        title = title_div.find("h1").string
        return title

    def get_chapters_urls(self) -> list[str]:
        chapter_links = self.web_data.find_all("a", class_="chapter-name")
        chapter_links.reverse()
        chapters_urls = [data["href"] for data in chapter_links]
        return chapters_urls

    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        chapter_title = data.find(class_="panel-chapter-info-top").find("h1").string
        formatted_chapter_title = utils.format_name(chapter_title)
        chapter_file = f"{index:04}_{formatted_chapter_title}.zip"
        chapter_path = os.path.join(self.directory_path, chapter_file)
        return chapter_path

    def get_images_urls(self, data: BeautifulSoup) -> list[str]:
        images = data.find(class_="container-chapter-reader").find_all("img")
        images_src = [img["src"] for img in images]
        return images_src

    def download_image(self, image_url: str) -> bytes:
        response = requests.get(image_url, headers=self.get_headers())
        return response.content

    def get_headers(self) -> dict[str, str]:
        basic_headers = super().get_headers().copy()
        basic_headers.update(self.EXTRA_HEADERS)
        return basic_headers

    # def get_images_data(self, url: str) -> BeautifulSoup:
    #     html_doc = DownloaderClient.get_data(url).text
    #     images_data = DownloaderClient.get_web_data(html_doc)
    #     return images_data

    # def get_images(self, chapter_url: str) -> list[Image]:
    #     images_data = self.get_images_data(chapter_url)
    #     scraped_data = images_data.select_one("div.container-chapter-reader").findChildren("img")
    #     images = [
    #         Image(number=index, source=data["src"], file=DownloaderClient.get_data(data["src"]).content)
    #         for index, data in enumerate(scraped_data, start=1)
    #     ]
    #     return images

    # def create_zip_file(self, dir_path: str, format: str, chapters: list[Chapter]) -> None:
    #     for chapter in chapters:
    #         file = f"{dir_path}/{chapter.number}. {chapter.name}.{format}"
    #         with ZipFile(file, "a") as zipf:
    #             for image in chapter.images:
    #                 zipf.write(image.file, image.number)


# basic_headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
#     "Accept": "image/avif,image/webp,*/*",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Connection": "keep-alive",
#     "Referer": "https://chapmanganato.com/",
#     "Sec-Fetch-Dest": "image",
#     "Sec-Fetch-Mode": "no-cors",
#     "Sec-Fetch-Site": "cross-site",
#     "Pragma": "no-cache",
#     "Cache-Control": "no-cache",
#     "TE": "trailers",
# }


"""

cuando tenemos un solo becario para hacer las cosas a mano:

voy a manganto.com
busco one piece
Crea una carpeta para el manga
para cada capitulo
    crea una carpeta para ese capitulo
    para cada imagen en el capitulo
        descargar en esa carpeta
    comprimir la carpeta en zip


cuando tenemos 20 becarios para hacer las cosas a mano:

voy a manganto.com
busco one piece
Crea una carpeta para el manga
Crea una lista de urls de capitulos
Divido el trabajo (cantidad de capitulos) entre el numero de becarios
- resultado: 1000 capitulos entre 20 becarios: 50
Cada becario se le asigna la cantidad de capitulos equivalente al resultado anterior, con eso debera:
    Entrar a la web de sus capitulos (con la url del capitulo) y:
        Descargar las imagenes del capitulo 
        Comprimir la carpeta en zip correspondiente al capitulo


funcion guardar capitulo comprimido: url de un capitulo -> produce un archivo zip en disco
    navegar en la url
    obtener el nombre del capitulo
    obtener la lista de urls de imagenes
    para cada imagen:
        descargar
    comprimir carpeta

"""
