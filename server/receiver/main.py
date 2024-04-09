import uvicorn
from path import Path
from fastapi import FastAPI
from server.receiver.config import settings
from server.receiver.tasks.routes import router


app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOCS_URL,
    openapi_url=settings.OPENAPI_URL,
)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(
        app=f'{Path(__file__).stem}:app',
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.UVICORN_RELOAD,
    )
