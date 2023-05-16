import asyncio
import json
import logging

from quart import Quart, request
from util.task import Task
from uuid import uuid1


BACKGROUND_TASKS = set()
app = Quart(__name__)


@app.get("/")
def get_hello_world():
    return "Hello world!"


@app.post("/tasks")
async def add_task_to_loop():
    job_payload = await request.get_json()
    task_item = Task(**job_payload)
    logging.debug(f"Received task of type: {task_item.task_type}")
    task_name = "{}_{}".format(task_item.task_type, uuid1())
    task = asyncio.create_task(task_item.exec(), name=task_name)
    BACKGROUND_TASKS.add(task)
    task.add_done_callback(BACKGROUND_TASKS.discard)
    pass


@app.get("/tasks")
async def get_all_queued_tasks():
    return json.dumps(list(BACKGROUND_TASKS))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=True)
