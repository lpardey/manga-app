# Standard Library
from abc import ABC, abstractmethod

# Local imports
from ..downloader.config import ChapterStrategyConfig
from .exceptions import DownloaderException
from .models import ChapterIndex


class ChapterSelectionStrategy(ABC):
    @abstractmethod
    def chapter_in_selection(self, chapter: ChapterIndex) -> bool:
        pass


class AllChaptersSelection(ChapterSelectionStrategy):
    def chapter_in_selection(self, _: ChapterIndex) -> bool:
        return True


class ChapterListSelection(ChapterSelectionStrategy):
    def __init__(self, chapters: list[ChapterIndex]) -> None:
        super().__init__()
        self.chapters = chapters

    def chapter_in_selection(self, chapter: ChapterIndex) -> bool:
        return chapter in self.chapters


class ChapterRangeSelection(ChapterSelectionStrategy):
    def __init__(self, lower_bound: ChapterIndex, upper_bound: ChapterIndex) -> None:
        super().__init__()
        self.lower_bound = float(self.remove_non_numeric(lower_bound))
        self.upper_bound = float(self.remove_non_numeric(upper_bound))
        if self.lower_bound > self.upper_bound:
            raise DownloaderException(
                f"Invalid range pattern. '{self.lower_bound}' is greater than '{self.upper_bound}'"
            )

    def chapter_in_selection(self, chapter: ChapterIndex) -> bool:
        return self.lower_bound <= float(self.remove_non_numeric(chapter)) <= self.upper_bound

    @staticmethod
    def remove_non_numeric(string: str) -> str:
        return "".join(char for char in string if char.isnumeric() or char == ".")


STRATEGIES: dict[str, type[ChapterSelectionStrategy]] = {
    "all": AllChaptersSelection,
    "list": ChapterListSelection,
    "range": ChapterRangeSelection,
}


def chapters_selection_factory(params: ChapterStrategyConfig) -> ChapterSelectionStrategy:
    return STRATEGIES[params.strategy](**params.config)
