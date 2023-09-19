from datetime import datetime, timedelta, timezone

from sources.classic.actors.scheduler import Scheduler


def func():
    print('done')
    return 15


scheduler = Scheduler()

scheduler.with_delay(5, func)
scheduler.run()

print('step 1')
