import queue
import threading

from .base import BaseActor
from .call import Call


class Actor(BaseActor):

    def loop(self) -> None:
        while not self._stopped:
            try:
                call: Call = self.inbox.get(timeout=0.01)
                call()
            except queue.Empty:
                pass
            except Exception as ex:
                self._logger.error(ex)

    def run(self) -> None:
        thread = threading.Thread(target=self.loop)
        thread.start()
