import time

from classic.actors import SuperVisor, actor
from classic.components import WeakSetRegistry

# глобальный реестр слабых ссылок акторов
registry = WeakSetRegistry()
supervisor = SuperVisor(registry=registry)


@actor(registry=supervisor.registry)
class MyCls:

    @actor.method
    def summa(sel, a, b):
        time.sleep(4)
        return a + b


if __name__ == '__main__':

    c = MyCls()
    print('id my cls = ', id(c))
    supervisor.run()

    print('start calc')
    r = c.summa(3, 4).get()
    print('result calc =  ', r)
    print('stop calc')
    r = c.summa(1, 2).get()
