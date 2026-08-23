from tasks.models import (
    Task,
    TaskCreate,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)


def test_create_task_model():
    request = TaskCreate(
        title="Complete onboarding",
        description="Submit required documents",
        priority=TaskPriority.HIGH,
    )

    task = Task(**request.model_dump())

    assert task.title == "Complete onboarding"
    assert task.description == "Submit required documents"
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.TODO
    assert task.id is not None
    assert task.created_at is not None


def test_default_task_values():
    request = TaskCreate(title="Read employee handbook")

    task = Task(**request.model_dump())

    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert task.description == ""


def test_task_update_model():
    update = TaskUpdate(
        status=TaskStatus.COMPLETED,
        priority=TaskPriority.LOW,
    )

    assert update.status == TaskStatus.COMPLETED
    assert update.priority == TaskPriority.LOW