from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ..models import TaskRequest, TaskResponse
from ..services.celery_worker import parse_url

router = APIRouter(prefix="/celery")


@router.post('/parsing', response_model=Annotated[TaskResponse, Depends()])
def create_task(data: Annotated[TaskRequest, Body()]):
    print('Try')
    task = parse_url.delay(data.url)
    print('task send')
    return TaskResponse(id=task.id)


@router.get('/parsing/{task_id}', response_model=Annotated[TaskResponse, Depends()])
def get_task(task_id: str):
    task = parse_url.AsyncResult(task_id)
    return TaskResponse(id=task.id, status=task.status, data=task.result)
