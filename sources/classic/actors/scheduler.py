import heapq
from dataclasses import Field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Union

from .actor import Actor
from .task import CronTask, OneTimeTask, PeriodicTask, Task


# @component
class Scheduler(Actor):
    _tasks: list[Task] = Field(default_factory=list)

    def _on_timeout(self):
        if self._tasks:
            task: Task = heapq.heappop(self._tasks)
            task.run_job()
            if task.next_run_time:
                heapq.heappush(self._tasks, task)

    @Actor.method
    def with_delay(self, delay: float, job: Callable[[], Any], name=None):
        date = datetime.now(timezone.utc) + timedelta(seconds=delay)
        task = OneTimeTask(date=date, job=job, name=name)
        heapq.heappush(self._tasks, task)

    @Actor.method
    def by_cron(self, schedule, job: Callable[[], Any], name=None):
        task = CronTask(schedule=schedule, job=job, name=name)
        heapq.heappush(self._tasks, task)

    @Actor.method
    def by_period(self,
                  delay: Union[timedelta, float],
                  job: Callable[[], Any],
                  name=None):
        task = PeriodicTask(period=delay, job=job, name=name)
        heapq.heappush(self._tasks, task)

    @Actor.method
    def cancel(self, task_name: str):
        for t in self._tasks:
            if t.name == task_name:
                del t
                heapq.heapify(self._tasks)
                break

    def _get_timeout(self):

        if len(self._tasks) < 1:
            return DEFAULT_TIMEOUT

        dt_next_task = self._tasks[0].next_run_time
        dt_current = datetime.now(timezone.utc)
        if dt_next_task < dt_current:
            return 0
        else:
            return (dt_next_task - dt_current).seconds
