import logging
import queue
import threading
from abc import ABC
from dataclasses import field
from typing import Any, Callable

from classic.components import component

from .primitives import Call, Future

STOP = 'STOP'  # сообщение посылаемое в inbox для остановки цикла актора


@component
class Actor(ABC):
    """
    Класс актора, который всегда выполняется в отдельном потоке.
    Потокобезопасен.
    """
    inbox: queue.Queue = field(default=None)  # BUG
    thread: threading.Thread = field(default=None)
    loop_timeout: float = 0.01

    _thread_name = None
    _stopped: bool = False

    def __post_init__(self):  # BUG
        self.inbox = queue.Queue()  # BUG

    def loop(self) -> None:
        """
        Основной рабочий цикл актора.
        """
        while not self._stopped:
            try:
                message = self.inbox.get(timeout=self._get_timeout())
                self._handle(message)
            except queue.Empty:
                self._on_timeout()
            except Exception as ex:
                logging.error(ex)

    def run(self):
        """
        Запускает цикл работы актора в отдельном потоке.
        Если поток упал - поднимает его.
        """
        if not self.thread:
            self.thread = threading.Thread(
                target=self.loop,
                name=self._thread_name,
            )

        if not self.thread.is_alive():
            self.thread.start()

    def stop(self):
        """
        Останавливает поток актора.
        """
        self.inbox.put(STOP)

    @staticmethod
    def method(method: Callable[[], Any]) -> Future:
        """
        Декоратор методов актора который делает их потокобезопасными.

        Args:
            method (Callable[[], Any]): Метод класса актора для декорирования.

        Returns:
            Future: Ссылка на будущий результат выполнения метода.
        """

        def wrapper(*args, **kwargs):
            call = Call(method, args, kwargs)
            args[0].inbox.put(call)
            return call.result

        return wrapper

    def _get_timeout(self) -> float:
        """
        Возвращает время ожидания поступлений сообщений
        в основном рабочем цикле.

        Returns:
            float: тайм-аут ожидания сообщений в inbox.
        """
        return self.loop_timeout

    def _handle(self, message: Any) -> None:
        """
        Обрабатывает сообщение которое послали актору в inbox.

        Args:
            message (Any): Сообщение отправленное в inbox.
        """
        if message is STOP:
            self._stopped = True
        elif isinstance(message, Call):
            message()
        else:
            self._on_unknown_message(message)

    def _on_timeout(self):
        """
        Обрабатывает истечение времени ожидания новых сообщений в inbox.
        """
        pass

    def _on_unknown_message(self, message: Any):
        """
        Обрабатывает неизвестный тип сообщений отправленных в inbox.

        Args:
            message (Any): Сообщение отправленное в inbox.
        """
        pass
