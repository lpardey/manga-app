# Standard Library
import logging
import os
from abc import ABC, abstractmethod
from pathlib import PurePath
from zipfile import ZipFile

# Dependencies
import aiohttp
import asyncio
from bs4 import BeautifulSoup

# Local imports
from . import utils
from .concurrency import gather_with_concurrency
from .models import ChapterIndex
from .config import DownloaderConfig

logger = logging.getLogger(__name__)


class Downloader(ABC):
    DOMAINS: set[str] = set()
    EXTRA_HEADERS: dict[str, str] = dict()

    def __init__(self, config: DownloaderConfig) -> None:
        super().__init__()
        self.config = config

    async def scrap_main_url(self, url: str | None) -> BeautifulSoup:
        url = url if url else self.config.url
        # crea un gestor de contextos para hacer la request
        async with aiohttp.ClientSession(headers=self.get_headers()) as session:
            async with session.get(url) as response:
                # pide el texto de la respuesta. como text es una corrutina,
                # hace falta ponerle un await delante para que te devuelva el
                # valor del texto. si no, lo que te devuelve es la corrutina en si.
                # no poner el await delante de una funcion asincrona es una de las
                # fuentes mas comunes de errores al implementar codigo asincrono
                html_doc = await response.text()
                web_data = BeautifulSoup(html_doc, "html.parser")
                return web_data

    def create_directory(self, dir_name: str) -> None:
        """Creates a directory on the path specified (default path: '.'). Returns directory path"""
        path = os.path.join(self.config.path, dir_name)
        if not os.path.isdir(path):
            os.makedirs(path)

    def get_headers(self) -> dict[str, str]:
        basic_headers = dict()
        basic_headers.update(self.EXTRA_HEADERS)
        return basic_headers

    def get_src_numbers_suffix(self, src: str) -> str:
        src_stem = PurePath(src).stem
        suffix = []
        for character in reversed(src_stem):
            if character.isnumeric():
                suffix.append(character)
            else:
                break
        suffix.reverse()
        src_numbers_suffix = "".join(suffix)
        return src_numbers_suffix

    def get_chapter_number_to_url(self, all_chapters: dict[ChapterIndex, str]) -> dict[ChapterIndex, str]:
        filtered_chapters = {
            chapter: url
            for chapter, url in all_chapters.items()
            if self.config.chapters_selection.chapter_in_selection(chapter)
        }
        return filtered_chapters

    async def download_image(self, image_url: str) -> bytes:
        """Downloads an image from a url and returns it as bytes"""
        async with aiohttp.ClientSession(headers=self.get_headers()) as session:
            async with session.get(image_url) as response:
                logger.info(f"Downloading image: {image_url}")
                image_data = await response.read()
                return image_data

    def get_image_name(self, index: int, image_url: str) -> str:
        image_basename = os.path.basename(image_url)
        image_extension = os.path.splitext(image_basename)[1]
        image_name = f"{index:04}{image_extension}"
        return image_name

    async def get_all_chapter_images(self, urls: list[str]) -> list[tuple[str, bytes]]:
        get_images_tasks = [self.download_image(url) for url in urls]
        images = await asyncio.gather(*get_images_tasks)
        image_names = [self.get_image_name(index, url) for index, url in enumerate(urls)]
        named_images = list(zip(image_names, images))
        return named_images

    async def download_chapter(self, data: BeautifulSoup, zipf: ZipFile) -> None:
        """Gets chapter data, creates a zip file by its name, and downloads and stores its images to the zip file"""
        images_urls = await self.get_images_src(data)
        # This could be done in parallel
        images = await self.get_all_chapter_images(images_urls)
        # this is a blocking operation
        for image_filename, image_data in images:
            zipf.writestr(image_filename, image_data)

    async def get_chapter_data(self, url) -> BeautifulSoup:
        async with aiohttp.ClientSession(headers=self.get_headers()) as session:
            async with session.get(url) as response:
                html_doc = await response.text()
                chapter_data = BeautifulSoup(html_doc, "html.parser")
                return chapter_data

    async def process_chapter(self, index: int, url: str, manga_title: str) -> None:
        chapter_data = await self.get_chapter_data(url)
        chapter_filename = self.get_chapter_filename(index, chapter_data)
        chapter_full_path = os.path.join(self.config.path, manga_title, chapter_filename)
        logger.info(f"Downloading chapter: {chapter_filename}")
        with ZipFile(chapter_full_path, "w") as zipf:
            await self.download_chapter(chapter_data, zipf)

    async def download(self) -> None:
        """Creates a directory and downloads chapters, in other words: MangaDanga!"""
        web_data = await self.scrap_main_url(url=None)
        title = self.get_title(web_data)
        sanitized_title = utils.format_name(title)
        self.create_directory(sanitized_title)
        all_chapters = self.get_all_chapters_to_url(web_data)
        chapter_number_to_url = self.get_chapter_number_to_url(all_chapters)
        chapters_tasks = [
            self.process_chapter(index, url, sanitized_title) for index, url in chapter_number_to_url.items()
        ]
        await gather_with_concurrency(self.config.threads, *chapters_tasks)

    @abstractmethod
    def get_title(self, data: BeautifulSoup) -> str:
        """Scrapes a title"""
        pass

    @abstractmethod
    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        """Scrapes chapter name. Returns its path with '.zip' extension"""
        pass

    @abstractmethod
    def get_images_src(self, data: BeautifulSoup) -> list[str]:
        """Scrapes images urls"""
        pass

    @abstractmethod
    def get_all_chapters_to_url(self, data: BeautifulSoup) -> dict[ChapterIndex, str]:
        """Scrapes chapters urls. Returns a dict of chapter index to chapters urls"""
        pass