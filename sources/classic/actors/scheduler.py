import heapq
import queue
import threading
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Union

from .base import BaseActor
from .call import Call
from .task import CronTask, OneTimeTask, PeriodicTask, Task

DEFAULT_TIMEOUT = 60


class Scheduler(BaseActor):

    def __init__(self) -> None:
        super().__init__()

        self._launch_plan = []

    def loop(self):
        while not self._stopped:
            try:
                timeout = self._get_timeout()
                task = self.inbox.get(block=True, timeout=timeout)
                self._add_task_to_heap(task)
            except queue.Empty:
                if self._launch_plan:
                    task: Task = heapq.heappop(self._launch_plan)
                    task.run_job()

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

        if len(self._launch_plan) < 1:
            return DEFAULT_TIMEOUT

        dt_next_task = self._launch_plan[0].get_next_run_time()
        dt_current = datetime.now(timezone.utc)
        if dt_next_task < dt_current:
            return 0
        else:
            return (dt_next_task - dt_current).seconds

    def _add_task_to_heap(self, task):
        if isinstance(task, Task):
            heapq.heappush(self._launch_plan, task)
        elif isinstance(task, str):
            for t in self._launch_plan:
                if t.name == task:
                    del t
                    heapq.heapify(self._launch_plan)
                    break
        else:
            raise Exception('Unknown type task')
