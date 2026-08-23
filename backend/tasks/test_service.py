from pathlib import Path
from uuid import uuid4

from backend.tasks.models import (
    TaskCreate,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)
from backend.tasks.repository import TaskRepository
from backend.tasks.service import TaskService


def create_service(tmp_path: Path) -> TaskService:
    repository = TaskRepository(tmp_path / "tasks.db")
    return TaskService(repository)


def test_create_task(tmp_path: Path):
    service = create_service(tmp_path)

    task = service.create_task(
        TaskCreate(
            title="Complete onboarding",
            description="Submit documents",
            priority=TaskPriority.HIGH,
        )
    )

    assert task.title == "Complete onboarding"
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.HIGH


def test_get_task(tmp_path: Path):
    service = create_service(tmp_path)

    created = service.create_task(
        TaskCreate(title="Read handbook")
    )

    retrieved = service.get_task(created.id)

    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.title == "Read handbook"


def test_list_tasks(tmp_path: Path):
    service = create_service(tmp_path)

    service.create_task(TaskCreate(title="Task 1"))
    service.create_task(TaskCreate(title="Task 2"))

    tasks = service.list_tasks()

    assert len(tasks) == 2


def test_update_task(tmp_path: Path):
    service = create_service(tmp_path)

    created = service.create_task(
        TaskCreate(
            title="Original title",
            priority=TaskPriority.LOW,
        )
    )

    updated = service.update_task(
        created.id,
        TaskUpdate(
            title="Updated title",
            priority=TaskPriority.HIGH,
        ),
    )

    assert updated is not None
    assert updated.title == "Updated title"
    assert updated.priority == TaskPriority.HIGH
    assert updated.status == TaskStatus.TODO


def test_update_missing_task(tmp_path: Path):
    service = create_service(tmp_path)

    result = service.update_task(
        uuid4(),
        TaskUpdate(title="Does not exist"),
    )

    assert result is None


def test_complete_task(tmp_path: Path):
    service = create_service(tmp_path)

    created = service.create_task(
        TaskCreate(title="Finish task")
    )

    completed = service.complete_task(created.id)

    assert completed is not None
    assert completed.status == TaskStatus.COMPLETED


def test_complete_missing_task(tmp_path: Path):
    service = create_service(tmp_path)

    result = service.complete_task(uuid4())

    assert result is None


def test_delete_task(tmp_path: Path):
    service = create_service(tmp_path)

    created = service.create_task(
        TaskCreate(title="Delete task")
    )

    deleted = service.delete_task(created.id)

    assert deleted is True
    assert service.get_task(created.id) is None


def test_delete_missing_task(tmp_path: Path):
    service = create_service(tmp_path)

    deleted = service.delete_task(uuid4())

    assert deleted is False

def test_update_task_preserves_types(tmp_path: Path):
    service = create_service(tmp_path)

    created = service.create_task(
        TaskCreate(title="Type safety test")
    )

    updated = service.update_task(
        created.id,
        TaskUpdate(
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.HIGH,
        ),
    )

    assert updated is not None
    assert updated.status == TaskStatus.COMPLETED
    assert updated.priority == TaskPriority.HIGH
    assert isinstance(updated.status, TaskStatus)
    assert isinstance(updated.priority, TaskPriority)