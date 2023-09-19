import heapq
import queue
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Union

from .base import BaseActor
from .task import CronTask, OneTimeTask, PeriodicTask, Task

DEFAULT_TIMEOUT = 60


class Scheduler(BaseActor):

    def __init__(self) -> None:
        super().__init__()

        self._task_q = []

    def loop(self):
        while not self._stopped:
            try:
                timeout = self._get_timeout()
                task = self.inbox.get(block=True, timeout=timeout)
                self._add_task_to_heap(task)
            except queue.Empty:
                if self._task_q:
                    task: Task = heapq.heappop(self._task_q)
                    task.run_job()

    def run(self):
        self.loop()

    def with_delay(self, delay: float, job: Callable[[], Any], name=None):
        date = datetime.now(timezone.utc) + timedelta(seconds=delay)
        task = OneTimeTask(date=date, job=job, name=name)
        self.inbox.put(task)

    def by_cron(self, schedule, job: Callable[[], Any], name=None):
        task = CronTask(schedule=schedule, job=job, name=name)
        self.inbox.put(task)

    def by_period(self,
                  delay: Union[timedelta, float],
                  job: Callable[[], Any],
                  name=None):
        task = PeriodicTask(period=delay, job=job, name=name)
        self.inbox.put(task)

    def cancel(self, task_name: str):
        self.inbox.put(task_name)

    def _get_timeout(self):
        if len(self._task_q) < 1:
            return DEFAULT_TIMEOUT

        dt_next_task = self._task_q[0].get_next_run_time()
        dt_current = datetime.now(timezone.utc)
        if dt_next_task < dt_current:
            return 0
        else:
            return (dt_next_task - dt_current).seconds

    def _add_task_to_heap(self, task):
        if isinstance(task, Task):
            heapq.heappush(self._task_q, task)
        elif isinstance(task, str):
            for t in self._task_q:
                if t.name == task:
                    del t
                    heapq.heapify(self._task_q)
                    break
        else:
            raise Exception('Unknown type task')
