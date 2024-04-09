from fastapi.testclient import TestClient
from pydantic import BaseModel
from server.receiver.main import app

client = TestClient(app)


class Task(BaseModel):
    id: int
    delay: float


def test_setTaskPositiveDelay():
    task = Task(id=1, delay=1)
    response = client.post(
        "/tasks/setTask",
        json=task.model_dump_json()
    )
    assert response.status_code == 201
    assert response.json() == {"asyncAnswer": "Ok"}


def test_setTaskZeroDelay():
    task = Task(id=1, delay=0)
    response = client.post(
        "/tasks/setTask",
        json=task.model_dump_json()
    )
    assert response.status_code == 201
    assert response.json() == {"asyncAnswer": "Ok"}


def test_setTaskNegativeDelay():
    task = Task(id=1, delay=-1)
    response = client.post(
        "/tasks/setTask",
        json=task.model_dump_json()
    )
    assert response.status_code == 422
