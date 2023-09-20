import time
import threading
from sources.classic.actors.actor import Actor, actor_method


def func(a, b):
    time.sleep(0)
    return a + b


# actor = Actor()
# actor.run()

# call1 = Call(func, (1, 2), {})
# feature1 = actor.inbox.put(call1)

# call2 = Call(func, (2, 3), {})
# feature2 = actor.inbox.put(call2)

# print('step 1')
# print(call1.result.get())
# print('step 2')
# print(call2.result.get())
# print('step 3')

# actor.stop()

# python -m examples.actor
# step 1
# 3
# step 2
# 5
# step 3
# >>> stop and exit python app...


# @actor
class SomeActor(Actor):

    @actor_method
    def some_method_1(self, a, b) -> int:
        return a + b


some_actor = SomeActor()
some_actor.run()

future = some_actor.some_method_1(1, 2)
result = future.get()
print('result = ', result)

print('main  thread = ', threading.get_ident())
print('actor thread = ', some_actor.get_ident_thread())

some_actor.stop()
