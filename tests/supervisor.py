from sources.classic.actors import Actor
from sources.classic.actors import Supervisor


class SomeClassOne(Actor):

    @Actor.method
    def some_method(self, a, b):
        return a / b


class SomeClassTwo(Actor):

    @Actor.method
    def some_method(self, a, b):
        return a * b


actor_1 = SomeClassOne()
actor_2 = SomeClassOne()
actor_3 = SomeClassTwo()

supervisor = Supervisor()
supervisor.add(actor_1)
supervisor.add(actor_2)
supervisor.run()
supervisor.add(actor_3)

future_1 = actor_1.some_method(4, 2)
print('result_1 = ', future_1.get())

# произойдет исключение
future_2 = actor_2.some_method(9, 0)
print('result_2 = ', future_2)  # не нужен get так как ответа не будет

future_3 = actor_3.some_method(4, 2)
print('result_3 = ', future_3.get())

# падание
# BUG как уронить поток?

# подъем
result_5 = actor_1.some_method(9, 2).get()
print('result_5 = ', result_5)

actor_1.stop()
actor_2.stop()
actor_3.stop()
supervisor.stop()
