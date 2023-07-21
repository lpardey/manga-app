from typing import Any
from pydantic import BaseModel


class ChapterStrategyConfig(BaseModel):
    strategy: str = "all"
    config: dict[str, Any] = {}


class DownloaderConfig(BaseModel):
    url: str = ""
    path: str = "."
    chapter_strategy: ChapterStrategyConfig = ChapterStrategyConfig()
    threads: int = 1
