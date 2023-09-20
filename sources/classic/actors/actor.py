import queue

from .base import BaseActor
from .call import Call
from .future import Future


def actor_method(method) -> Future:

    def wrapper(*args, **kwargs):
        call = Call(method, args, kwargs)
        args[0].inbox.put(call)
        return call.result

    return wrapper


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
