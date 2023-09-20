import threading

from sources.classic.actors.actor import Actor
from sources.classic.actors.base import BaseActor

threading.excepthook


class Supervisor(BaseActor):

    def __init__(self) -> None:
        super().__init__()

    def add(self, actor: Actor):
        pass

    def remove(self):
        pass
