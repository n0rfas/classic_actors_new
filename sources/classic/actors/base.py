import logging
import queue
import threading
from abc import ABC, abstractmethod
from sources.classic.actors.call import Call

LOGGER_PREFIX = 'evraz.actor'


class BaseActor(ABC):

    def __init__(self) -> None:
        self.inbox = queue.Queue()  # RW он точно публичный?

        self._logger = logging.getLogger(LOGGER_PREFIX)
        self._stopped = False
        self._thread = None

    @abstractmethod
    def loop(self):  # RW он точно публичный?
        ...

    def run(self):
        if not self._thread:
            self._thread = threading.Thread(target=self.loop)

        if not self._thread.is_alive():
            self._thread.start()

    def run_in_background(self):
        self.loop()

    def stop(self):
        self._stopped = True

    def get_ident_thread(self):
        call = Call(threading.get_ident, (), {})
        self.inbox.put(call)
        return call.result.get()
