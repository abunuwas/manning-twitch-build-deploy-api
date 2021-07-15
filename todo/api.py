import datetime
import uuid
from uuid import UUID

from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from todo.server import server
from todo.schemas import ListTasksSchema, CreateTaskSchema, GetTaskSchema

TODO = []


@server.get('/todo', response_model=ListTasksSchema)
def get_tasks():
    return {
        'tasks': TODO
    }


@server.post('/todo', status_code=status.HTTP_201_CREATED, response_model=GetTaskSchema)  # noqa: E501
def create_task(payload: CreateTaskSchema):
    task = payload.dict()
    task['id'] = uuid.uuid4()
    task['created'] = datetime.datetime.now()
    task['status'] = task['status'].value
    task['priority'] = task['priority'].value
    TODO.append(task)
    return task


@server.get('/todo/{task_id}', response_model=GetTaskSchema)
def get_task(task_id: UUID):
    for task in TODO:
        if task['id'] == task_id:
            return task
    raise HTTPException(
        status_code=404, detail=f'Task with ID {task_id} not found'
    )


@server.put('/todo/{task_id}', response_model=GetTaskSchema)
def update_task(task_id: UUID, payload: CreateTaskSchema):
    for task in TODO:
        if task['id'] == task_id:
            task.update(payload.dict())
            task['status'] = task['status'].value
            task['priority'] = task['priority'].value
            return task
    raise HTTPException(
        status_code=404, detail=f'Task with ID {task_id} not found'
    )


@server.delete('/todo/{task_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_task(task_id: UUID):
    for index, task in enumerate(TODO):
        if task['id'] == task_id:
            TODO.pop(index)
            return
    raise HTTPException(
        status_code=404, detail=f'Order with ID {task_id} not found'
    )
