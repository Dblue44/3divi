import logging
from datetime import datetime
import aiohttp
import pika
from pydantic import BaseModel, Field
from server.receiver.config import settings
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


class QueueTask(Task):
    receiveTime: str


class TaskResponse(BaseModel):
    asyncAnswer: str = Field(default="ok")


@router.post("/setTask", response_model=TaskResponse)
async def setTask(task: Task) -> Response:
    queueTask = QueueTask(id=task.id, delay=task.delay, receiveTime=f"{datetime.now()}")
    logger.info("Отправка запроса на запись в db2.txt")
    async with aiohttp.ClientSession() as session:
        await session.post(url=settings.WRITER_URL, json=queueTask.model_dump())
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()
    logger.info("Отправка задачи в очередь")
    channel.basic_publish(
        exchange='',
        routing_key='tasks_queue',
        body=queueTask.model_dump_json(),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )

    connection.close()
    return Response(status_code=status.HTTP_201_CREATED, content=TaskResponse().model_dump_json())
