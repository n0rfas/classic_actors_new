import logging
import queue
import threading
from abc import ABC
from typing import Any

from sources.classic.actors.primitives import Call

from .future import Future

LOGGER_PREFIX = 'evraz.actor'

STOP = 'STOP'


class Actor(ABC):
    inbox: queue.Queue
    thread: threading.Thread
    loop_timeout: float = 0.01

    _stopped: bool

    def loop(self) -> None:
        while not self._stopped:
            try:
                message = self.inbox.get(timeout=self._get_timeout())
                self._handle(message)
            except queue.Empty:
                self._on_timeout()
            except Exception as ex:
                logging.error(ex)

    def _on_timeout(self):
        pass

    def _on_unknown_message(self, message: Any):
        pass

    def _get_timeout(self):
        return self.loop_timeout

    def _handle(self, message):
        if message is STOP:
            self._stopped = True
        elif isinstance(message, Call):
            message()
        else:
            self._on_unknown_message(message)

    def run(self):
        if not self.thread:
            self.thread = threading.Thread(target=self.loop)

        if not self.thread.is_alive():
            self.thread.start()

    def stop(self):
        self.inbox.put(STOP)

    @staticmethod
    def method(method) -> Future:

        def wrapper(*args, **kwargs):
            call = Call(method, args, kwargs)
            args[0].inbox.put(call)
            return call.result

        return wrapper
