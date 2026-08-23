from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from backend.tasks.models import Task, TaskCreate, TaskUpdate
from backend.tasks.repository import TaskRepository
from backend.tasks.service import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


def get_task_service() -> TaskService:
    return TaskService(TaskRepository())


@router.post(
    "",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    return service.create_task(task_data)


@router.get(
    "",
    response_model=list[Task],
)
def list_tasks(
    service: TaskService = Depends(get_task_service),
):
    return service.list_tasks()


@router.get(
    "/{task_id}",
    response_model=Task,
)
def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
):
    task = service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.patch(
    "/{task_id}",
    response_model=Task,
)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    task = service.update_task(task_id, task_data)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.post(
    "/{task_id}/complete",
    response_model=Task,
)
def complete_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
):
    task = service.complete_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
):
    deleted = service.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )