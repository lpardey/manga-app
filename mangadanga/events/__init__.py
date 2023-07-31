from typing import Any, Callable
from queue import Queue
import logging

logger = logging.getLogger("EventManager")


class EventManager:
    def __init__(self):
        self.running = False
        self.events_queue: Queue[tuple[str, tuple, dict[str, Any]]] = Queue()
        self.listeners: dict[str, list[Callable[..., None]]] = dict()

    def subscribe(self, event: str, listener: Callable[..., None]):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(listener)

    def unsubscribe(self, event: str, listener: Callable[..., None]):
        if event in self.listeners:
            self.listeners[event].remove(listener)

    def emit(self, event: str, *args, **kwargs):
        logger.info(f"Emitting event {event}")
        self.events_queue.put((event, args, kwargs))

    def process_event(self, event, *args, **kwargs):
        if event in self.listeners:
            for listener in self.listeners[event]:
                try:
                    listener(*args, **kwargs)
                except Exception as e:
                    logger.exception(f"Exception raised while processing event {event}: {e}")
        else:
            logger.warning(f"Event {event} has no listeners")

    def process_queue(self):
        while not self.events_queue.empty():
            event, args, kwargs = self.events_queue.get()
            logger.info(f"Processing event for {event}")
            self.process_event(event, *args, **kwargs)

    def stop(self):
        self.running = False

    def purge_events(self):
        self.events_queue = Queue()


EVENT_MANAGER = EventManager()


class Event:
    NAME = None

    def __init__(self, manager: EventManager = EVENT_MANAGER):
        self.manager = manager

    def emit(self, *args, **kwargs):
        if self.NAME is None:
            raise NotImplementedError("An event needs a name...")
        self.manager.emit(self.NAME, *args, **kwargs)

    def subscribe(self, listener: Callable[..., None]):
        self.manager.subscribe(self.NAME, listener)


class OnCloseProgress(Event):
    NAME = "close_progress"

    def emit(self):
        self.manager.emit(self.NAME)

    def subscribe(self, listener: Callable[[], None]):
        self.manager.subscribe(self.NAME, listener)


class EventCaca(Event):
    NAME = "caca"

    def emit(self, color: str, cantidad: float, consistencia: str):
        self.manager.emit(self.NAME, color, cantidad, consistencia)

    def subscribe(self, listener: Callable[[str, float, str], None]):
        self.manager.subscribe(self.NAME, listener)
