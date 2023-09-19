import heapq
import logging
from datetime import datetime, timedelta, timezone
from queue import Empty, Queue
from typing import Any, Callable, List, Optional, Tuple, Union

from .task import PeriodicTask, Task, OneTimeTask, CronTask

LOGGER_PREFIX = 'evraz.scheduler'
DEFAULT_TIMEOUT = 60

Job = Callable[[], Any]


class Scheduler():

    def __init__(self) -> None:
        self.inbox = Queue()

        self._logger = logging.getLogger(LOGGER_PREFIX)
        self._stopped = False
        self._task_q = []

    def with_delay(self, delay: float, job: Job, name=None):
        date = datetime.now(timezone.utc) + timedelta(seconds=delay)
        task = OneTimeTask(date=date, job=job, name=name)
        self.inbox.put(task)

    def by_cron(self, schedule, job: Job, name=None):
        task = CronTask(schedule=schedule, job=job, name=name)
        self.inbox.put(task)

    def by_period(self, delay: Union[timedelta, float], job: Job, name=None):
        task = PeriodicTask(period=delay, job=job, name=name)
        self.inbox.put(task)

    def cancel(self, task_name: str):
        self.inbox.put(task_name)

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

    def run(self) -> None:
        while not self._stopped:
            try:
                # waiting for new planned_task to be added
                timeout = self._get_timeout()
                task = self.inbox.get(block=True, timeout=timeout)
                self._add_task_to_heap(task)
            except Empty:
                # get and run next task
                if self._task_q:
                    task: Task = heapq.heappop(self._task_q)
                    task.run_job()
            except Exception as ex:
                self._logger.error(ex)

    def stop(self) -> None:
        self._stopped = True

    def _get_timeout(self):
        if len(self._task_q) < 1:
            return DEFAULT_TIMEOUT

        dt_next_task = self._task_q[0].get_next_run_time()
        is_overdue_gap_needed = self._task_q[0].is_overdue_gap_needed

        dt_current = datetime.now(timezone.utc)

        if dt_next_task < dt_current:
            return 0
        else:
            return (dt_next_task - dt_current).seconds


"""
def schedules(cls):
    return cls


def by_cron(cls):
    return cls


def by_period(cls):
    return cls


def with_delay(cls):
    return cls


@schedules
class SomeClass:

    @by_cron('* * * * *')
    def some_method(self):
        pass

    @by_period(10.5)
    def some_method(self):
        pass

    @with_delay(timedelta)
    def some_method(self):
        pass

    @with_delay(23)
    def some_method(self):
        pass
"""
