import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    WRITER_URL: str = "http://writer:80/tasks/writeTaskFirst"

    # RabbitMQ
    RABBITMQ_DEFAULT_USER: str = os.environ['RABBITMQ_DEFAULT_USER']
    RABBITMQ_DEFAULT_PASS: str = os.environ['RABBITMQ_DEFAULT_PASS']
    RABBITMQ_URL: str = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbitmq:5672/%2F"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
