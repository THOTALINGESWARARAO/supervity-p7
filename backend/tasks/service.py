from uuid import UUID

from backend.tasks.models import Task, TaskCreate, TaskStatus, TaskUpdate
from backend.tasks.repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task_data: TaskCreate) -> Task:
        task = Task(**task_data.model_dump())
        return self.repository.create(task)

    def get_task(self, task_id: UUID) -> Task | None:
        return self.repository.get(task_id)

    def list_tasks(self) -> list[Task]:
        return self.repository.list_all()

    def update_task(
        self,
        task_id: UUID,
        task_data: TaskUpdate,
    ) -> Task | None:
        existing_task = self.repository.get(task_id)

        if existing_task is None:
            return None

        update_data = task_data.model_dump(
            exclude_unset=True,
            mode="json",
        )

        updated_data = existing_task.model_dump(
            mode="json"
        )

        updated_data.update(update_data)

        updated_task = Task.model_validate(updated_data)

        self.repository.update(updated_task)

        return updated_task

    def complete_task(self, task_id: UUID) -> Task | None:
        existing_task = self.repository.get(task_id)

        if existing_task is None:
            return None

        completed_task = existing_task.model_copy(
            update={"status": TaskStatus.COMPLETED}
        )

        self.repository.delete(task_id)
        self.repository.create(completed_task)

        return completed_task

    def delete_task(self, task_id: UUID) -> bool:
        return self.repository.delete(task_id)