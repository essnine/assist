from asyncio import sleep
from loguru import logger
from croniter import croniter
from datetime import datetime
from enum import Enum
# import json   # importing these for preparing task dump functionality
# import pickle


class TaskType(Enum):
    ONEOFF = 1
    CRON = 2


class TaskState(Enum):
    PENDING = -1
    QUEUED = 0
    RUNNING = 1
    SUCCESSFUL = 2
    FAILED = 3


""" for my own reference, this is what each value in a cron expression
means
<minute> <hour> <day-of-month> <month> <day-of-week>
"""

class SimpleTask:
    def __init__(self, task_type: TaskType, name: str, cron_expr: str = ""):
        self.task_type = task_type
        self.name = name
        self.state: TaskState = 0
        self.cron_expr = cron_expr
        if task_type == 2:
            if len(cron_expr) == 0:
                raise Exception("setting cronjob required cron expr")

    def dump_task(self):
        pass

    def __str__(self):
        return str((self.name, {
            "name": self.name,
            "state": self.state,
            "cron_expr": self.cron_expr,
        }))

    async def run(self):
        """This isn't perfect, but it should work
        """
        if not self.state == 1:
            self.state = 1
        else:
            print("task {} is already running".format(self.name))
        try:
            while True:
                if self.task_type == 2:
                    if not croniter.match(self.cron_expr, datetime.now()):
                        await sleep(60)
                        continue
                    await self.exec()
                else:
                    await self.exec()
                    break
        except Exception as exc:
            logger.error(f"Task failed due to error: {str(exc)}")
            logger.exception(exc)
            self.state = 3
        else:
            self.state = 2
        logger.info("Task Ended")

    async def exec(self):
        logger.info("Running Sample Task")
        pass

