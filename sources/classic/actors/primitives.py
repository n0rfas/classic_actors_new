from dataclasses import dataclass, field
from queue import Queue
from typing import Any, Callable, Dict, Tuple


@dataclass
class Future:

    output: Queue[Any] = field(
        default_factory=lambda: Queue(1),
        init=False,
    )

    def set(self, value: Any) -> None:
        self.output.put(value)

    def get(self, timeout=None) -> Any:
        return self.output.get(block=True, timeout=timeout)

    def check(self):
        return self.output.get(block=False)


@dataclass
class Call:
    function: Callable[..., Any]
    args: Tuple[Any]
    kwargs: Dict[str, Any]

    result: Future = field(default_factory=Future)

    def __call__(self):
        result = self.function(*self.args, **self.kwargs)
        self.result.set(result)
