from typing import Any, Callable
from queue import Queue
import logging

logger = logging.getLogger("EventManager")


class EventManager:
    def __init__(self) -> None:
        self.running = False
        self.events_queue: Queue[tuple[str, tuple, dict[str, Any]]] = Queue()
        self.listeners: dict[str, list[Callable[..., None]]] = dict()

    def subscribe(self, event: str, listener: Callable[..., None]) -> None:
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(listener)

    def unsubscribe(self, event: str, listener: Callable[..., None]) -> None:
        if event in self.listeners:
            self.listeners[event].remove(listener)

    def emit(self, event: str, *args, **kwargs) -> None:
        logger.info(f"Emitting event {event}")
        self.events_queue.put((event, args, kwargs))

    def process_event(self, event, *args, **kwargs) -> None:
        if event in self.listeners:
            for listener in self.listeners[event]:
                try:
                    listener(*args, **kwargs)
                except Exception as e:
                    logger.exception(f"Exception raised while processing event {event}: {e}")
        else:
            logger.warning(f"Event {event} has no listeners")

    def process_queue(self) -> None:
        while not self.events_queue.empty():
            event, args, kwargs = self.events_queue.get()
            logger.info(f"Processing event for {event}")
            self.process_event(event, *args, **kwargs)

    def stop(self) -> None:
        self.running = False

    def purge_events(self) -> None:
        self.events_queue = Queue()


EVENT_MANAGER = EventManager()


class Event:
    NAME = None

    def __init__(self, manager: EventManager = EVENT_MANAGER) -> None:
        self.manager = manager

    def emit(self, *args, **kwargs) -> None:
        if self.NAME is None:
            raise NotImplementedError("An event needs a name...")
        self.manager.emit(self.NAME, *args, **kwargs)

    def subscribe(self, listener: Callable[..., None]) -> None:
        self.manager.subscribe(self.NAME, listener)

    def unsubscribe(self, listener: Callable[..., None]) -> None:
        self.manager.unsubscribe(self.NAME, listener)


# Progress window events
class OnCloseProgress(Event):
    NAME = "close_progress"


class OnMangaInfoUpdate(Event):
    NAME = "manga_info_updated"


class OnChapterDownloadFinished(Event):
    NAME = "chapter_download_finished"


# Download button events
class OnDownloadFinished(Event):
    NAME = "download_finished"


class OnDownloadFinishedGUI(Event):
    NAME = "download_finished_gui"


class OnStartDownload(Event):
    NAME = "start_download"


# Main Window events
class OnQuit(Event):
    NAME = "quit"
