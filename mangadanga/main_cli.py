import logging
import sys
import asyncio

from .downloader import (
    DownloaderConfig,
    chapters_selection_factory,
    downloader_factory,
)
from .parser import get_parser


logger = logging.getLogger("MangaDanga")


def get_config(argv: list[str] = sys.argv[1:]) -> DownloaderConfig:
    parser = get_parser()
    args = parser.parse_args(argv)
    logger.info(args)
    # TODO: Refactor in order for CLI to work again
    chapters = chapters_selection_factory(args.chapters, args.chapter_range)
    downloader_config = DownloaderConfig(
        url=args.url, path=args.path, chapters_selection=chapters, threads=args.threads
    )
    return downloader_config


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    config = get_config()
    logger.info(f"Using configuration: {config}")
    downloader = downloader_factory(config)
    asyncio.run(downloader.download())


if __name__ == "__main__":
    main()
