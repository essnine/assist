import asyncio
import sys

from typing import Optional, List
from util.task import Task


TASK_QUEUE: List[Optional[Task]] = []


async def load_task_loop():
    while True:
        if not len(TASK_QUEUE):
            print("sleeping for a bit...")
            asyncio.sleep(2)
            continue
        task: Task = TASK_QUEUE[0]
        print(task.name)
        print(task.queue)
    print("exiting...")


def main():
    print("starting up")
    try:
        asyncio.run(load_task_loop())
    except Exception as exc:
        print(
            "Failed to start with error: {}\nExiting...".format(str(exc))
        )
        print(exc)
        if len(TASK_QUEUE):
            print("Dumping task queue to disk...")
            # TODO: implement backup mechanism here
        sys.exit()


if __name__ == "__main__":
    main()
