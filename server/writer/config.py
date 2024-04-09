from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Uvicorn
    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 80
    UVICORN_RELOAD: bool = True

    # FastAPI
    API_V1_STR: str = '/api/v1'
    TITLE: str = '3DiVi_Writer'
    VERSION: str = '0.0.1'
    DESCRIPTION: str = '3DiVi_Writer'
    DOCS_URL: str | None = f'{API_V1_STR}/docs'
    REDOCS_URL: str | None = f'{API_V1_STR}/redocs'
    OPENAPI_URL: str | None = f'{API_V1_STR}/openapi'


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
