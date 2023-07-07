from .models import ChapterIndex
from abc import ABC, abstractmethod
from .exceptions import DownloaderExceptionInvalidPattern


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
    @staticmethod
    def remove_non_numeric(string: str) -> str:
        return "".join(char for char in string if char.isnumeric() or char == ".")

    def __init__(self, lower_bound: ChapterIndex, upper_bound: ChapterIndex) -> None:
        super().__init__()
        self.lower_bound = float(self.remove_non_numeric(lower_bound))
        self.upper_bound = float(self.remove_non_numeric(upper_bound))
        if self.lower_bound > self.upper_bound:
            raise DownloaderExceptionInvalidPattern()

    def chapter_in_selection(self, chapter: float) -> bool:
        return self.lower_bound <= float(self.remove_non_numeric(chapter)) <= self.upper_bound


def chapters_selection_factory(
    chapters: list[str] | None,
    chapter_range: tuple[str, str] | None,
) -> ChapterSelectionStrategy:
    if chapters is None and chapter_range is None:
        return AllChaptersSelection()
    if chapters is not None:
        return ChapterListSelection(chapters)
    return ChapterRangeSelection(*chapter_range)
