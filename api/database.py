from fastapi import FastAPI, HTTPException
from api.models import Task
import uuid


class DBSession:
    tasks = {}

    def __init__(self):
        self.tasks = DBSession.tasks

    def function_read_tasks(self, completed: bool):
        if completed is None:
            return self.tasks
        return {
            uuid_: item
            for uuid_, item in self.tasks.items() if item.completed == completed
        }

    def function_create_task(self, item: Task):
        uuid_ = uuid.uuid4()
        self.tasks[uuid_] = item
        return uuid_

    def function_read_task(self, uuid_: uuid.UUID):
        try:
            return self.tasks[uuid_]
        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception

    def function_replace_task(self, uuid_: uuid.UUID, item: Task):
        try:
            if(self.tasks[uuid_] == None):
                raise Exception
            self.tasks[uuid_] = item
        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception

    def function_alter_task(self, uuid_: uuid.UUID, item: Task):
        try:
            update_data = item.dict(exclude_unset=True)
            self.tasks[uuid_] = self.tasks[uuid_].copy(update=update_data)
        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception

    def function_remove_task(self, uuid_: uuid.UUID):
        try:
            del self.tasks[uuid_]
        except KeyError as exception:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            ) from exception


def get_db():
    return DBSession()
