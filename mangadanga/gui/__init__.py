from .style import GUIStyle
from .widgets import MainWindow
from .mangadanga_gui import MangadangaGUI
from .events import (
    EventManager,
    EVENT_MANAGER,
    Event,
    OnCloseProgress,
    OnMangaInfoUpdate,
    OnChapterDownloadFinished,
    OnDownloadFinished,
    OnDownloadFinishedGUI,
    OnStartDownload,
)

__all__ = [
    "GUIStyle",
    "MainWindow",
    "MangadangaGUI",
    "EventManager",
    "EVENT_MANAGER",
    "Event",
    "OnCloseProgress",
    "OnMangaInfoUpdate",
    "OnChapterDownloadFinished",
    "OnDownloadFinished",
    "OnDownloadFinishedGUI",
    "OnStartDownload",
]
