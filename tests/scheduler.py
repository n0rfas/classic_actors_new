import time

from sources.classic.actors.actor import Actor, actor_method
from sources.classic.actors.scheduler import Scheduler


def func():
    print('function')
    return 15


scheduler = Scheduler()
scheduler.run()
# scheduler.with_delay(1, func)
# scheduler.by_period(5, func)
# scheduler.by_cron('* * * * *', func)


class SomeActor(Actor):

    @actor_method
    def func(self):
        print('method')
        return 13

    @actor_method
    def mistake_func(self, a, b):
        return a + b


some_actor = SomeActor()
some_actor.run()

task_name = 'test_by_period'
scheduler.by_period(3, some_actor.func, name=task_name)
time.sleep(16)
scheduler.cancel(task_name)
some_actor.stop()
time.sleep(6)
scheduler.stop()
