from typing import Type
import urllib.parse
from .exceptions import DownloaderExceptionUrlWithoutCoverage
from .base import Downloader, DownloaderConfig
from .drivers import Mangadoom, Manganato, Mangatown, Asurascans


DOWNLOADERS: set[Type[Downloader]] = {
    Mangadoom,
    Manganato,
    Mangatown,
    Asurascans,
}


def get_domain(url: str) -> str:
    domain = urllib.parse.urlparse(url).netloc
    return domain


def downloader_factory(config: DownloaderConfig, downloaders: set[Type[Downloader]] = DOWNLOADERS) -> Downloader:
    domain = get_domain(config.url)
    for downloader_cls in downloaders:
        if domain in downloader_cls.DOMAINS:
            return downloader_cls(config)
    raise DownloaderExceptionUrlWithoutCoverage()
