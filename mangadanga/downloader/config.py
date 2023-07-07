from pydantic import BaseModel
from .chapter_selection import AllChaptersSelection, ChapterSelectionStrategy


class DownloaderConfig(BaseModel):
    url: str
    chapters_selection: ChapterSelectionStrategy = AllChaptersSelection()
    path: str = "."
    threads: int = 1

    class Config:
        arbitrary_types_allowed = True
