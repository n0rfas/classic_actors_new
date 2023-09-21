import queue
import threading
from dataclasses import field
from typing import Any

from classic.components import component

from sources.classic.actors.actor import Actor


@component
class Supervisor(Actor):
    """
    Супервизор акторов. Запускает, останавливает, поднимает при падении.
    """
    # имя потока супервизора
    _thread_name = 'supervisor'
    # словарь акторов где ключ это id процесса актора
    actors: dict[int, Actor] = field(default_factory=dict)
    # обработчик не перехваченного исключения метода Thread.run()
    default_excepthook: Any = field(default=None)

    def __post_init__(self):
        self.inbox = queue.Queue()  # BUG
        # подменяем обработчик при падении потока нашим обработчиком
        self.default_excepthook = threading.excepthook
        threading.excepthook = self.excepthook

    def __del__(self):
        # при удалении супервизора возвращаем обработчик падающих потоков
        threading.excepthook = self.default_excepthook

    @Actor.method
    def add(self, actor: Actor):
        """
        Добавляет актор в супервизор для отслеживания и запускает его.

        Args:
            actor (Actor): Экземпляр актора.
        """
        actor.run()
        self.actors[actor.thread.ident] = actor

    @Actor.method
    def remove(self, actor):
        """
        Удаляет актор из супервизор для отслеживания.

        Args:
            actor (Actor): Экземпляр актора.
        """
        if ident := actor.thread.ident in self.actors:
            del self.actors[ident]

    def excepthook(self, args):
        """
        Наш обработчик не перехваченных исключений потока.

        Args:
            args (_type_): Аргументы упавшего потока.
        """
        # в хук может не придти поток - пропускаем это
        if not args.thread:
            return

        # если упавший поток это наш актор - перезапускаем его
        if actor := self.actors.get(args.thread.ident):
            actor.run()

        self.default_excepthook(args)

    # BUG при вызове стоп нужно останавливать все потоки?
    # def stop(self):
    #     pass
