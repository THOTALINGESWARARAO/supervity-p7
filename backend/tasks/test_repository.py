from datetime import datetime
from pathlib import Path
from uuid import uuid4

from backend.tasks.models import Task, TaskPriority, TaskStatus
from backend.tasks.repository import TaskRepository

def test_create_and_get_task(tmp_path: Path):
    repository = TaskRepository(tmp_path / "tasks.db")

    task = Task(
        title="Complete onboarding",
        description="Submit required documents",
        priority=TaskPriority.HIGH,
    )

    created = repository.create(task)
    retrieved = repository.get(task.id)

    assert created.id == task.id
    assert retrieved is not None
    assert retrieved.title == "Complete onboarding"
    assert retrieved.description == "Submit required documents"
    assert retrieved.priority == TaskPriority.HIGH
    assert retrieved.status == TaskStatus.TODO


def test_list_tasks(tmp_path: Path):
    repository = TaskRepository(tmp_path / "tasks.db")

    first = Task(title="First task")
    second = Task(title="Second task")

    repository.create(first)
    repository.create(second)

    tasks = repository.list_all()

    assert len(tasks) == 2
    assert {task.id for task in tasks} == {first.id, second.id}


def test_get_missing_task_returns_none(tmp_path: Path):
    repository = TaskRepository(tmp_path / "tasks.db")

    result = repository.get(uuid4())

    assert result is None


def test_delete_task(tmp_path: Path):
    repository = TaskRepository(tmp_path / "tasks.db")

    task = Task(title="Delete me")
    repository.create(task)

    deleted = repository.delete(task.id)

    assert deleted is True
    assert repository.get(task.id) is None


def test_delete_missing_task_returns_false(tmp_path: Path):
    repository = TaskRepository(tmp_path / "tasks.db")

    deleted = repository.delete(uuid4())

    assert deleted is False