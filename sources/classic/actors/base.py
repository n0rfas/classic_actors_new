import logging
import queue
from abc import ABC, abstractmethod

LOGGER_PREFIX = 'evraz.actor'


class BaseActor(ABC):

    def __init__(self) -> None:
        self.inbox = queue.Queue()

        self._logger = logging.getLogger(LOGGER_PREFIX)
        self._stopped = False

    @abstractmethod
    def loop(self):
        ...

    @abstractmethod
    def run(self):
        ...

    def stop(self):
        self._stopped = True
