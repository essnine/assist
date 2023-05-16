import asyncio
import json
import uvicorn
import importlib

from loguru import logger
from quart import Quart, request
from util.task import SimpleTask
from util.runner import process_task
from uuid import uuid1


BACKGROUND_TASKS = set()
app = Quart(__name__)


@app.route("/", methods=["GET"])
def get_hello_world():
    return "Hello world!"


@app.route("/tasks", methods=["POST"])
async def add_task_to_loop():
    try:
        job_payload = await request.get_json()
        task_class = job_payload.get("taskClass")
        logger.debug(f"Received task of type: {task_class}")
        task, task_name = process_task(**job_payload)
        BACKGROUND_TASKS.add(task)
        task.add_done_callback(BACKGROUND_TASKS.discard)
        return {"taskName": task_name, "message": "", "success": True}, 200
    except Exception as exc:
        logger.exception(exc)
        return {"message": str(exc), "success": False}, 422


@app.route("/tasks", methods=["GET"])
async def get_all_queued_tasks():
    # logger.info(json.dumps([str(i) for i in asyncio.all_tasks()], indent=4))
    return json.dumps([str(i) for i in BACKGROUND_TASKS]), 200


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8090, log_level="info")
