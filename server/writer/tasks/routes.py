import os.path
import time
import logging
from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import (
    status,
    APIRouter,
    Response
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    handlers=[
        logging.FileHandler("logs.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["tasks"], prefix="/tasks")


class Task(BaseModel):
    id: int
    delay: float = Field(ge=0)
    receiveTime: str


@router.post("/writeTaskFirst")
async def writeTaskFirst(task: Task) -> Response:
    if not os.path.exists(f"db1.txt"):
        logger.info("Создание db1.txt")
        with open("db1.txt", "w") as f:
            f.write("| id | receive_time | write_time |\n")
    logger.info(f"Запись в db1.txt задачи {task.id}")
    with open("db1.txt", "a") as f:
        f.write(f"| {task.id} | {task.receiveTime} | {datetime.now()} |\n")
    return Response(status_code=status.HTTP_200_OK)


@router.post("/writeTaskSecond")
async def writeTaskSecond(task: Task) -> Response:
    if not os.path.exists(f"db2.txt"):
        logger.info("Создание db2.txt")
        with open("db2.txt", "w") as f:
            f.write("| id | receive_time |\n")
    logger.info(f"Запись в db2.txt задачи {task.id}")
    with open("db2.txt", "a") as f:
        f.write(f"| {task.id} | {task.receiveTime} |\n")
    return Response(status_code=status.HTTP_200_OK)
