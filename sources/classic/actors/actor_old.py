from dataclasses import dataclass, field
from functools import wraps
from queue import Queue
from typing import Any, Callable, Dict, Tuple

from classic.components import Registry, add_extra_annotation, component

from .future import Future


@dataclass
class Call:
    function: Callable[[Any], Any]
    args: Tuple[Any]
    kwargs: Dict[str, Any]

    result: Future = field(default_factory=Future)

    def __call__(self):
        result = self.function(*self.args, **self.kwargs)
        self.result.set(result)


def method(function):

    @wraps(function)
    def wrapper(self, *args, **kwargs):
        call = Call(function, *args, **kwargs)
        self.inbox.put(call)
        return call.result

    add_extra_annotation(wrapper, 'inbox', Queue)

    return wrapper


def group(cls, size: int):
    return [cls() for __ in range(size)]


def is_actor(obj):
    return getattr(obj, '__is_actor__', False)


def actor(cls):
    cls.__is_actor__ = True
    cls.__annotations__['registry'] = Registry
    return component(cls)


actor.method = method
