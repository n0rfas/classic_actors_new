import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Optional, Union

from croniter import croniter

LOGGER_PREFIX = 'evraz.task'


class Task(ABC):

    def __init__(
        self,
        job: Callable[[], None],
        args: tuple = None,
        kwargs: dict = None,
        name: Optional[str] = None,
        is_overdue_gap_needed: bool = True,
    ) -> None:
        self._logger = logging.getLogger(LOGGER_PREFIX)
        self._job = job
        self._args = args or None
        self._kwargs = kwargs or None
        self._name = name
        self._is_overdue_gap_needed = is_overdue_gap_needed

    @property
    @abstractmethod
    def next_run_time(self) -> datetime:
        ...

    def run_job(self) -> Any:
        self._logger.info(
            'Task [%s] started with schedule [%s]',
            self._name,
            self._next_run_time,
        )

        try:
            self._job(*self._args, **self._kwargs)
        except Exception as ex:
            self._logger.exception(
                'Unexpected error occurred in task [%s]: "%s".',
                self._name,
                ex,
            )
        else:
            self._logger.info('Task completed [%s]', self._name)

    def __lt__(self, other) -> bool:
        return self._next_run_time < other._next_run_time

    def __gt__(self, other) -> bool:
        return self._next_run_time > other._next_run_time


class OneTimeTask(Task):

    def __init__(self, date: datetime, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._next_run_time = datetime

    def set_next_run_time(self) -> None:
        self._next_run_time = None


class CronTask(Task):

    def __init__(self, schedule: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._schedule = croniter(schedule, datetime.now(timezone.utc))
        self._next_run_time = next(self._schedule)

    def set_next_run_time(self) -> None:
        self._next_run_time = next(self._schedule)


class PeriodicTask(Task):

    def __init__(self, period: Union[timedelta, float], *args,
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._period = period if isinstance(period, timedelta) else timedelta(
            seconds=period)
        self._next_run_time = datetime.now(timezone.utc)

    def set_next_run_time(self) -> None:
        self._next_run_time += self._period
