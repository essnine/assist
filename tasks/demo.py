from loguru import logger
from util.task import SimpleTask, TaskType
from asyncio import sleep


class Demo(SimpleTask):
    def __init__(
        self,
        task_type: TaskType,
        name: str,
        payload: dict = {},
    ):
        super(SimpleTask, self).__init__()
        self.payload = payload
        self.task_type = task_type
    
    async def exec(self):
        logger.info(self.payload)
        logger.info("Demo Task sleeps for 5 seconds")
        await sleep(5.0)
        print("OK")
        logger.info("Demo Task Over")
        pass
