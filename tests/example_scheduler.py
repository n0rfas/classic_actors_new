from datetime import datetime, timedelta, timezone

from sources.classic.actors.scheduler import Scheduler


def func():
    print('time= ', datetime.now(timezone.utc).time())


scheduler = Scheduler()

scheduler.by_period(10, func)

scheduler.run()

print('end')
