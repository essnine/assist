import asyncio
import tasks
from uuid import uuid1


def process_task(taskClass, payload):
    TaskClass = getattr(tasks, taskClass, None)
    if TaskClass is None:
        raise Exception(f"Could not find task {TaskClass}")
    task_item = TaskClass(**payload)
    task_name = "{}_{}".format(task_item.task_type, uuid1())
    task = asyncio.create_task(task_item.exec(), name=task_name)
    return task, task_name
