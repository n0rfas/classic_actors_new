from sources.classic.actors import Actor
from sources.classic.actors import Scheduler


def func():
    print('function')
    return 15


class SomeActor(Actor):

    @Actor.method
    def func(self, a, b):
        print('a + b =', a + b)


scheduler = Scheduler()
scheduler.with_delay(1, func)
scheduler.by_period(5, func)
scheduler.by_cron('* * * * *', func)
scheduler.run()

some_actor = SomeActor()
some_actor.run()
scheduler.by_period(
    2,
    some_actor.func,
    args=(2, 6),
    task_name='some_actor_task',
)
