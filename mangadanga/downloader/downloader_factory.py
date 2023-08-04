# Standard Library
import urllib.parse

# Local imports
from .base import Downloader, DownloaderConfig
from .drivers import Asurascans, Mangadoom, Manganato, Mangatown
from .exceptions import DownloaderException

DOWNLOADERS: set[type[Downloader]] = {
    Mangadoom,
    Manganato,
    Mangatown,
    Asurascans,
}


def downloader_factory(config: DownloaderConfig, downloaders: set[type[Downloader]] = DOWNLOADERS) -> Downloader:
    domain = get_domain(config.url)
    try:
        downloader_cls = next(downloader for downloader in downloaders if domain in downloader.DOMAINS)
        return downloader_cls(config)
    except StopIteration:
        valid_urls: list[str] = sum((list(downloader.DOMAINS) for downloader in downloaders), start=[])
        message_lines = (
            [
                f"'{config.url}' is not covered (yet) by Mangadanga.",
                "",
                "Valid domain names:",
            ]
            + [" - " + valid_url for valid_url in valid_urls]
            + ["", "Our door is always open for a good cup of coffee!", "buymeacoffee@needmoney.co"]
        )
        message = "\n".join(message_lines)
        raise DownloaderException(message)


def get_domain(url: str) -> str:
    domain = urllib.parse.urlparse(url).netloc
    return domain
