from dataclasses import dataclass, field
from queue import Queue
from typing import Any, Callable, Dict, Tuple
from evraz.classic.components import component
from .future import Future


@dataclass
class Call:
    function: Callable[..., Any]
    args: Tuple[Any]
    kwargs: Dict[str, Any]

    result: Future = field(default_factory=Future)

    def __call__(self):
        result = self.function(self, *self.args, **self.kwargs)
        self.result.set(result)


def actor(cls):
    cls.inbox = field(default_factory=Queue)
    cls.__annotations__['inbox'] = Queue
    return component(cls)


def actor_method(function):

    def wrapper(self, *args, **kwargs):
        call = Call(function, args, kwargs)
        self.inbox.put(call)
        return call.result

    return wrapper


actor.method = actor_method
