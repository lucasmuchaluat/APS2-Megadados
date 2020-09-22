from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)


def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_get_right_task():
    response = client.post(
        "/task", json={"description": "test", "completed": False})
    assert response.status_code == 200
    response1 = client.get(f"/task/{response.json()}")
    assert response1.status_code == 200
    assert response1.json() == {"description": "test", "completed": False}
    response2 = client.delete(f"/task/{response.json()}")
    assert response2.status_code == 200
    assert response2.json() == None


def test_get_wrong_task():
    wrong_uuid = uuid.uuid4()
    response = client.get(f"/task/{wrong_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_get_task_list_even_empty():
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == {}


def test_get_whole_task_list():
    # cria
    response = client.post(
        "/task", json={"description": "test", "completed": False})
    assert response.status_code == 200
    response1 = client.post(
        "/task", json={"description": "test 1", "completed": True})
    assert response1.status_code == 200
    # get
    response2 = client.get("/task")
    assert response2.status_code == 200
    assert response2.json() == {response.json(): {"description": "test", "completed": False}, response1.json(): {
        "description": "test 1", "completed": True}}
    # apaga
    response3 = client.delete(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == None
    response4 = client.delete(f"/task/{response1.json()}")
    assert response4.status_code == 200
    assert response4.json() == None


def test_get_tasks_completed():
    # cria
    response = client.post(
        "/task", json={"description": "test", "completed": False})
    assert response.status_code == 200
    response1 = client.post(
        "/task", json={"description": "test 1", "completed": True})
    assert response1.status_code == 200
    # get
    response2 = client.get("/task?completed=True")
    assert response2.status_code == 200
    assert response2.json() == {response1.json(): {
        "description": "test 1", "completed": True}}
    # apaga
    response3 = client.delete(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == None
    response4 = client.delete(f"/task/{response1.json()}")
    assert response4.status_code == 200
    assert response4.json() == None


def test_get_tasks_not_completed():
    # cria
    response = client.post(
        "/task", json={"description": "test", "completed": False})
    assert response.status_code == 200
    response1 = client.post(
        "/task", json={"description": "test 1", "completed": True})
    assert response1.status_code == 200
    # get
    response2 = client.get("/task?completed=False")
    assert response2.status_code == 200
    assert response2.json() == {response.json(): {
        "description": "test", "completed": False}}
    # apaga
    response3 = client.delete(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == None
    response4 = client.delete(f"/task/{response1.json()}")
    assert response4.status_code == 200
    assert response4.json() == None


def test_delete_right_task():
    response = client.post(
        "/task", json={"description": "test", "completed": "False"})
    assert response.status_code == 200
    response_ = client.delete(f"/task/{response.json()}")
    assert response_.status_code == 200
    assert response_.json() == None


def test_delete_wrong_task():
    wrong_uuid = uuid.uuid4()
    response = client.delete(f"/task/{wrong_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
