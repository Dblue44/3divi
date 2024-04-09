import json
import time
import aiohttp
import asyncio
import pika
from pydantic import BaseModel, Field
from config import settings


class Task(BaseModel):
    id: int
    delay: float = Field(ge=0)
    receiveTime: str


async def process_order(task: dict) -> None:
    time.sleep(task["delay"])
    async with aiohttp.ClientSession() as session:
        await session.post(url=settings.WRITER_URL, json=task)


def start_task(ch, method, properties, body) -> None:
    task = json.loads(body)
    asyncio.run(process_order(task))
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
channel = connection.channel()

channel.queue_declare(queue='tasks_queue', durable=True)
channel.basic_consume(queue='tasks_queue', on_message_callback=start_task)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
