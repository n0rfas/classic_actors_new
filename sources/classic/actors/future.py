from dataclasses import dataclass, field
from queue import Queue
from typing import Any


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
