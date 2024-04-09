import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Uvicorn
    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 80
    UVICORN_RELOAD: bool = True

    # FastAPI
    API_V1_STR: str = '/api/v1'
    TITLE: str = '3DiVi_Receiver'
    VERSION: str = '0.0.1'
    DESCRIPTION: str = '3DiVi_Receiver'
    DOCS_URL: str | None = f'{API_V1_STR}/docs'
    REDOCS_URL: str | None = f'{API_V1_STR}/redocs'
    OPENAPI_URL: str | None = f'{API_V1_STR}/openapi'

    WRITER_URL: str = "http://writer:80/tasks/writeTaskSecond"

    # RabbitMQ
    RABBITMQ_DEFAULT_USER: str = os.environ['RABBITMQ_DEFAULT_USER']
    RABBITMQ_DEFAULT_PASS: str = os.environ['RABBITMQ_DEFAULT_PASS']
    RABBITMQ_URL: str = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbitmq:5672/%2F"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
