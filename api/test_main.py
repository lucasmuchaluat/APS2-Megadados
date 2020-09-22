from fastapi.testclient import TestClient
from .main import app
import uuid

client = TestClient(app)

# test if a non existing route returns an error
def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

# test if the service is getting one single task correctly
def test_get_right_task():
    # create task
    response = client.post(
        "/task", json={"description": "test", "completed": False})
    assert response.status_code == 200
    # get task
    response1 = client.get(f"/task/{response.json()}")
    assert response1.status_code == 200
    # deleting task
    assert response1.json() == {"description": "test", "completed": False}
    response2 = client.delete(f"/task/{response.json()}")
    assert response2.status_code == 200
    assert response2.json() == None

# test if the service is dealing with correctly when quering a non existing task
def test_get_wrong_task():
    # generates a nonexisting uuid
    wrong_uuid = uuid.uuid4()
    response = client.get(f"/task/{wrong_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

# test if the service is dealing correctly when trying to get a task from a not valid uuid
def test_get_not_formated_uuid():
    # create non existing uuid
    false_uuid = "uuu"
    #tries to get task
    response = client.get(f"/task/{false_uuid}")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'uuid_'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}]}

# test if the service returns a empty task list when its empty
def test_get_task_list_even_empty():
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == {}

# test if the service returns a list of all created tasks
def test_get_whole_task_list():
    # create task
    response = client.post(
        "/task", json={"description": "test", "completed": False})
    assert response.status_code == 200

    # create task
    response1 = client.post(
        "/task", json={"description": "test 1", "completed": True})
    assert response1.status_code == 200
    # get list
    response2 = client.get("/task")
    assert response2.status_code == 200
    assert response2.json() == {response.json(): {"description": "test", "completed": False}, response1.json(): {
        "description": "test 1", "completed": True}}

    # delete task
    response3 = client.delete(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == None

    # delete task
    response4 = client.delete(f"/task/{response1.json()}")
    assert response4.status_code == 200
    assert response4.json() == None

# test if the service returns a list of completed tasks
def test_get_tasks_completed():
    # create task
    response = client.post(
        "/task", json={"description": "test", "completed": False})
    assert response.status_code == 200

    # create task
    response1 = client.post(
        "/task", json={"description": "test 1", "completed": True})
    assert response1.status_code == 200

    # get the list of completed tasks
    response2 = client.get("/task?completed=True")
    assert response2.status_code == 200
    assert response2.json() == {response1.json(): {
        "description": "test 1", "completed": True}}
    
    # delete task
    response3 = client.delete(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == None

    # delete task
    response4 = client.delete(f"/task/{response1.json()}")
    assert response4.status_code == 200
    assert response4.json() == None

# test if the service returns a list of not completed tasks
def test_get_tasks_not_completed():
    # create task
    response = client.post(
        "/task", json={"description": "test", "completed": False})
    assert response.status_code == 200

    # create task
    response1 = client.post(
        "/task", json={"description": "test 1", "completed": True})
    assert response1.status_code == 200

    # get the list of not completed tasks
    response2 = client.get("/task?completed=False")
    assert response2.status_code == 200
    assert response2.json() == {response.json(): {
        "description": "test", "completed": False}}

    # delete task
    response3 = client.delete(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == None

    # delete task
    response4 = client.delete(f"/task/{response1.json()}")
    assert response4.status_code == 200
    assert response4.json() == None

# test if the service is deleting a task correctly
def test_delete_right_task():
    # create task
    response = client.post(
        "/task", json={"description": "test", "completed": "False"})
    assert response.status_code == 200

    # delete task
    response_ = client.delete(f"/task/{response.json()}")
    assert response_.status_code == 200
    assert response_.json() == None

# test if the service is dealing correctly when trying to delete a non existing task
def test_delete_wrong_task():
    # create non existing uuid
    wrong_uuid = uuid.uuid4()
    #tries to delete task
    response = client.delete(f"/task/{wrong_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

# test if the service is dealing correctly when trying to delete a task from a not valid uuid
def test_delete_not_formated_uuid():
    # create non existing uuid
    false_uuid = "uuu"
    #tries to delete task
    response = client.delete(f"/task/{false_uuid}")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'uuid_'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}]}

#===
def test_create_delete_task():
    response = client.post(
        "/task", json={"description": "Buy baby diapers", "completed": False})
    assert response.status_code == 200

    response = client.delete(f"/task/{response.json()}")
    assert response.status_code == 200
    assert response.json() == None

# test if the service is refreshing a valid task when there is a correct patch request
def test_right_patch_task():
    # create task
    response_1 = client.post(
        "/task", json={"description": "Buy baby diapers", "completed": False})
    assert response_1.status_code == 200

    # refresh task
    response = client.patch(
        f"/task/{response_1.json()}", json={"description": "Buy baby diapers", "completed": True})
    assert response.status_code == 200
    assert response.json() == None

    # check if it refreshed correctly
    response = client.get(f"/task/{response_1.json()}")
    assert response.status_code == 200
    assert response.json() == {
        "description": "Buy baby diapers", "completed": True}

    # delete task
    response = client.delete(f"/task/{response_1.json()}")
    assert response.status_code == 200
    assert response.json() == None

# test if the service returns 405 if there is a patch request with a wrong endpoint
def test_patch_not_allowed():
    response = client.patch("/task")
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}

# test if the service returns 422 if there is a patch request with a not formated ID
def test_patch_not_formated_uuid():
    false_uuid = "huhuhuh"
    response = client.patch(
        f"/task/{false_uuid}", json={"description": "Buy baby diapers", "completed": True})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'uuid_'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}]}

# test if the service returns 404 if there is a patch request with wrong ID
def test_patch_wrong_uuid():
    not_uuid = uuid.uuid4()
    response = client.patch(
        f"/task/{not_uuid}", json={"description": "Buy baby diapers", "completed": True})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}

# test if the service is refreshing a valid task when there is a correct put request
def test_right_put_task():
    # create task
    response_1 = client.post(
        "/task", json={"description": "Buy baby diapers", "completed": False})
    assert response_1.status_code == 200

    # refresh task
    response = client.put(f"/task/{response_1.json()}",
                          json={"description": "Buy baby diapers", "completed": True})
    assert response.status_code == 200
    assert response.json() == None

    # check if it refreshed correctly
    response = client.get(f"/task/{response_1.json()}")
    assert response.status_code == 200
    assert response.json() == {
        "description": "Buy baby diapers", "completed": True}

    # delete task
    response = client.delete(f"/task/{response_1.json()}")
    assert response.status_code == 200
    assert response.json() == None

# test if the service returns 405 if there is a put request with a wrong endpoint
def test_put_not_allowed():
    response = client.put("/task")
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}

# test if the service returns 422 if there is a put request with a not formated ID
def test_put_not_formated_uuid():
    false_uuid = "huhuhuh"
    response = client.put(
        f"/task/{false_uuid}", json={"description": "Buy baby diapers", "completed": True})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': [
        'path', 'uuid_'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}]}

# test if the service returns 404 if there is a put request with a wrong ID
def test_put_wrong_uuid():
    wrong_uuid = uuid.uuid4()
    response = client.put(
        f"/task/{wrong_uuid}", json={"description": "Buy baby diapers", "completed": True})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}
