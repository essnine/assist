import logging

from enum import Enum
# import json   # importing these for preparing task dump functionality
# import pickle


class TaskType(Enum):
    SYNC = 1
    ASYNC = 2
    CRON = 3


class TaskState(Enum):
    PENDING = -1
    QUEUED = 0
    RUNNING = 1
    SUCCESSFUL = 2
    FAILED = 3


class Task:
    def __init__(self, task_type: TaskType, name: str):
        self.task_type = task_type
        self.name = name
        self.state: TaskState = 0
        pass

    def dump_task(self):
        pass

    def run(self):
        if not self.state == 1:
            self.state = 1
        else:
            print("task {} is already running".format(self.name))
        try:
            self.exec()
        except Exception as exc:
            logging.error(f"Task failed due to error: {str(exc)}")
            logging.exception(exc)
            self.state = 3
        else:
            self.state = 2

    def exec(self):
        pass
