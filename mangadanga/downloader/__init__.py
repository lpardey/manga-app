from .base import Downloader

from .drivers import (
    Mangadoom,
    Manganato,
    Mangatown,
    Asurascans,
)

from .chapter_selection import (
    ChapterSelectionStrategy,
    ChapterListSelection,
    ChapterRangeSelection,
    AllChaptersSelection,
    chapters_selection_factory,
)

from .config import DownloaderConfig

from .downloader_factory import DOWNLOADERS, downloader_factory

from .exceptions import (
    DownloaderException,
    DownloaderExceptionUrlWithoutCoverage,
    DownloaderExceptionInvalidPattern,
    DownloaderExceptionUnexpected,
)

from .concurrency import gather_with_concurrency


__all__ = [
    # .base
    "Downloader",
    # .drivers
    "Mangadoom",
    "Manganato",
    "Mangatown",
    "Asurascans",
    # .chapter_selection
    "ChapterSelectionStrategy",
    "AllChaptersSelection",
    "ChapterListSelection",
    "ChapterRangeSelection",
    "chapters_selection_factory",
    # .config
    "DownloaderConfig",
    # .downloader_factory
    "downloader_factory",
    "DOWNLOADERS",
    # .exceptions
    "DownloaderException",
    "DownloaderExceptionUrlWithoutCoverage",
    "DownloaderExceptionInvalidPattern",
    "DownloaderExceptionUnexpected",
    # .concurrence
    "gather_with_concurrency",
]
