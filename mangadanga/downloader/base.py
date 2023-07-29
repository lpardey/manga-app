# Standard Library
import logging
import os
from abc import ABC, abstractmethod
from pathlib import PurePath
from zipfile import ZipFile
import time

# Dependencies
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from mangadanga.downloader.exceptions import DownloaderException


from mangadanga.events import EVENT_MANAGER, EventManager

# Local imports
from . import utils
from .concurrency import gather_with_concurrency
from .models import ChapterIndex
from .config import DownloaderConfig
from .chapter_selection import chapters_selection_factory

logger = logging.getLogger(__name__)


class Downloader(ABC):
    DOMAINS: set[str] = set()
    EXTRA_HEADERS: dict[str, str] = dict()

    def __init__(self, config: DownloaderConfig, event_manager: EventManager = EVENT_MANAGER) -> None:
        super().__init__()
        self.config = config
        self.chapter_selection_strategy = chapters_selection_factory(config.chapter_strategy)
        self.event_manager = event_manager

    async def scrape_url(self, url: str) -> BeautifulSoup:
        # Creates a context manager to execute the request
        async with aiohttp.ClientSession(headers=self.get_headers()) as session:
            async with session.get(url) as response:
                # The "ignore" parameter is used to ignore encoding errors
                html_doc = await response.text("utf-8", "ignore")
                web_data = BeautifulSoup(html_doc, "html.parser")
                return web_data

    def create_directory(self, dir_name: str) -> None:
        """Creates a directory on the path specified (default path: '.'). Returns directory path"""
        path = os.path.join(self.config.path, dir_name)
        if not os.path.isdir(path):
            os.makedirs(path)

    @classmethod
    def get_headers(cls) -> dict[str, str]:
        basic_headers = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate"}
        basic_headers.update(cls.EXTRA_HEADERS)
        return basic_headers

    def get_src_numbers_suffix(self, src: str) -> str:
        """
        Receives an image url and returns the numbers at the end of the filename
        example: https://example.com/image_001.jpg -> 001
        """
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
            if self.chapter_selection_strategy.chapter_in_selection(chapter)
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
        images = await self.get_all_chapter_images(images_urls)
        for image_filename, image_data in images:
            zipf.writestr(image_filename, image_data)

    async def process_chapter(self, index: int, chapter_url: str, manga_title: str) -> None:
        chapter_data = await self.scrape_url(chapter_url)
        chapter_filename = self.get_chapter_filename(index, chapter_data)
        chapter_full_path = os.path.join(self.config.path, manga_title, chapter_filename)
        logger.info(f"Downloading chapter: {chapter_filename}")
        with ZipFile(chapter_full_path, "w") as zipf:
            await self.download_chapter(chapter_data, zipf)
        self.event_manager.emit("chapter_download_finished")

    # TODO: Independent decorators for logger and for time.time()
    async def download(self) -> None:
        """Creates a directory and downloads chapters, in other words: MangaDanga!"""
        try:
            status = "success"
            message = ""
            logger.info(f"Scrapping information for: {self.config.url}")
            web_data = await self.scrape_url(self.config.url)
            title = self.get_title(web_data)
            logger.info(f"Title: {title}")
            sanitized_title = utils.format_name(title)
            self.create_directory(sanitized_title)
            scrap_chapters_info_start = time.time()
            all_chapters = self.get_all_chapters_to_url(web_data)
            scrap_chapters_info_end = time.time()
            ellapsed_time = scrap_chapters_info_end - scrap_chapters_info_start
            logger.info(f"Scrapped chapters info in: {ellapsed_time:.2f} seconds")
            logger.info(f"Starting download for: {title}")
            download_chapters_start = time.time()
            chapter_number_to_url = self.get_chapter_number_to_url(all_chapters)
            chapters_tasks = [
                self.process_chapter(index, url, sanitized_title) for index, url in chapter_number_to_url.items()
            ]
            self.event_manager.emit("manga_info_updated", len(chapters_tasks))
            await gather_with_concurrency(self.config.threads, *chapters_tasks)
            download_chapters_end = time.time()
            ellapsed_time = download_chapters_end - download_chapters_start
            logger.info(f"Finished downloading: {title} in {ellapsed_time:.2f} seconds")
            average_time_per_chapter = ellapsed_time / len(chapter_number_to_url)
            logger.info(f"Average time per chapter: {average_time_per_chapter:.2f} seconds")
        except DownloaderException as e:
            status = "error"
            message = str(e)
            logger.exception(e)
        except Exception as e:
            status = "error"
            message = str(e)
            logger.exception(e)
        finally:
            self.event_manager.emit("download_finished", status, message)

    @abstractmethod
    def get_title(self, data: BeautifulSoup) -> str:
        """Scrapes a title"""
        pass

    @abstractmethod
    def get_chapter_filename(self, index: int, data: BeautifulSoup) -> str:
        """Scrapes chapter name. Returns its path with '.zip' extension"""
        pass

    @abstractmethod
    async def get_images_src(self, data: BeautifulSoup) -> list[str]:
        """Scrapes images urls"""
        pass

    @abstractmethod
    def get_all_chapters_to_url(self, data: BeautifulSoup) -> dict[ChapterIndex, str]:
        """Scrapes chapters urls. Returns a dict of chapter index to chapters urls"""
        pass
