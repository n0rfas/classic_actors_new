import time
from sources.classic.actors.actor import Actor
from sources.classic.actors.call import Call


def func(a, b):
    time.sleep(2.5)
    return a + b


actor = Actor()
actor.run()

call1 = Call(func, (1, 2), {})
feature1 = actor.inbox.put(call1)

call2 = Call(func, (2, 3), {})
feature2 = actor.inbox.put(call2)

print('step 1')
print(call1.result.get())
print('step 2')
print(call2.result.get())
print('step 3')

actor.stop()

# python -m examples.actor
# step 1
# 3
# step 2
# 5
# step 3
# >>> stop and exit python app...
