import threading
from dataclasses import Field
from typing import Any
from sources.classic.actors.actor import Actor


# @component
class Supervisor(Actor):
    actors: dict[int, Actor] = Field(default_factory=dict)
    old_excepthook: Any = Field(init=False)

    def __post_init__(self):
        self.old_excepthook = threading.excepthook
        threading.excepthook = self.excepthook

    @Actor.method
    def add(self, actor: Actor):
        self.actors[actor.thread.ident] = actor
        actor.run()

    @Actor.method
    def remove(self, actor):
        if ident := actor.thread.ident in self.actors:
            del self.actors[ident]

    def excepthook(self, args):
        if not args.thread:
            return

        if actor := self.actors.get(args.thread.ident):
            actor.run()

        self.old_excepthook(args)

    def __del__(self):
        threading.excepthook = self.old_excepthook
