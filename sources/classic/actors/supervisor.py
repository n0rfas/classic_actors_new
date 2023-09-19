from threading import Thread
from time import sleep
import queue
import logging
from .actors import Call, actor


def loop(actor):
    while True:
        try:
            call: Call = actor.inbox.get(timeout=0.001)
            call()
        except queue.Empty:
            pass
        except Exception as ex:
            logging.error(ex)


@actor
class SuperVisor:

    def __post_init__(self) -> None:
        self.threads = []

    @actor.method
    def add(self, actor):
        # добавляем новый поток для актора
        thread = Thread(target=loop, args=(actor, ), name=str(id(actor)))
        self.threads.append(thread)
        thread.start()

    @actor.method
    def remove(self, actor):
        # удаляем не нужный поток
        for thread in self.threads:
            if thread.name == str(id(actor)):
                self.threads.remove(thread)
                thread.stop()
                return

        raise Exception('Thread not found.')

    # @actor.periodic(0.001)  # TODO
    def check_threads(self):
        # поддерживаем жизнь в потоках
        for thread in self.threads:
            if not thread.is_alive():
                thread.start()

    def run(self):
        while True:
            try:
                call: Call = actor.inbox.get(timeout=0.001)
                call()
            except queue.Empty:
                pass
            except Exception as ex:
                logging.error(ex)

    def wait(self):
        # TODO подождать всех акторов
        pass

    def run_in_background(self):
        supervisor_thread = Thread(
            target=self.run,
            name='supervisor_thread',
        )
        supervisor_thread.start()
