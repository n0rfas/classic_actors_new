import time

from sources.classic.actors import Actor


class SomeClass(Actor):

    @Actor.method
    def some_method_1(self, a, b):
        return a + b

    @Actor.method
    def some_method_2(self, a, b):
        return a * b


some_class = SomeClass()
some_class.run()

future1 = some_class.some_method_1(1, 2)
result1 = future1.get()
print('result 1 = ', result1)

future2 = some_class.some_method_2(2, 3)
time.sleep(1)  # без задержки будет исключение
result2 = future2.check()
print('result 2 = ', result2)

some_class.stop()
