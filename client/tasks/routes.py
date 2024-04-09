import asyncio
import random
from typing import List

import aiohttp

from client.config import settings
from client.logger import logger
from pydantic import BaseModel, Field
from fastapi import (
    status,
    APIRouter,
    Response
)

router = APIRouter(tags=["tasks"], prefix="/tasks")


class Task(BaseModel):
    id: int
    delay: float = Field(ge=0)


class TasksData(BaseModel):
    connection_count: int = Field(ge=0)
    connection_value: int = Field(ge=0)
    delay_range: float = Field(ge=0)


async def sendTask(task: Task) -> None:
    async with aiohttp.ClientSession() as session:
        request = await session.post(url=settings.RECEIVER_URL, json=task.model_dump())
        logger.info(f"Send task {task.model_dump_json()}. Thread: {asyncio.current_task()}. Request: {request}")


@router.post("/setTask")
async def setTask(tasks: TasksData) -> Response:
    for i in range(tasks.connection_count):
        task = asyncio.create_task(
            sendTask(
                Task(id=i, delay=random.randint(0, tasks.delay_range))
            )
        )
        await task
    return Response(status=status.HTTP_201_CREATED, content={"asyncAnswer": "ok"})
