# Standard Library
from typing import Any
from pathlib import Path

# Dependencies
from pydantic import BaseModel


class ChapterStrategyConfig(BaseModel):
    strategy: str = "all"
    config: dict[str, Any] = {}


class DownloaderConfig(BaseModel):
    url: str = ""
    path: Path = Path(".")
    chapter_strategy: ChapterStrategyConfig = ChapterStrategyConfig()
    threads: int = 1
