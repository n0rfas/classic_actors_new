from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Tuple

from .future import Future


@dataclass
class Call:
    function: Callable[..., Any]
    args: Tuple[Any]
    kwargs: Dict[str, Any]

    result: Future = field(default_factory=Future)

    def __call__(self):
        result = self.function(*self.args, **self.kwargs)
        self.result.set(result)
