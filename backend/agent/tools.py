from uuid import UUID

from backend.ingestion.retrieve import search as rag_search
from backend.tasks.models import TaskCreate, TaskUpdate
from backend.tasks.repository import TaskRepository
from backend.tasks.service import TaskService


def get_task_service() -> TaskService:
    """Create a task service backed by the application's SQLite repository."""
    return TaskService(TaskRepository())


def search_hr_documents(
    query: str,
    top_k: int = 3,
    score_threshold: float | None = None,
) -> list[dict]:
    """Search the HR knowledge base using semantic retrieval."""
    return rag_search(
        query=query,
        top_k=top_k,
        score_threshold=score_threshold,
    )


def create_task(
    title: str,
    description: str = "",
    priority: str = "medium",
    due_date: str | None = None,
) -> dict:
    """Create a task through the existing task service."""

    if not due_date:
        due_date = None

    task_data = TaskCreate(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
    )

    task = get_task_service().create_task(task_data)

    return task.model_dump(mode="json")


def list_tasks() -> list[dict]:
    """Return all tasks through the existing task service."""

    tasks = get_task_service().list_tasks()

    return [
        task.model_dump(mode="json")
        for task in tasks
    ]


def update_task(
    task_id: str,
    title: str | None = None,
    description: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    due_date: str | None = None,
) -> dict | None:
    """Update a task through the existing task service."""

    update_data = {}

    if title is not None:
        update_data["title"] = title

    if description is not None:
        update_data["description"] = description

    if status is not None:
        update_data["status"] = status

    if priority is not None:
        update_data["priority"] = priority

    if due_date is not None:
        update_data["due_date"] = due_date

    task_data = TaskUpdate(**update_data)

    task = get_task_service().update_task(
        UUID(task_id),
        task_data,
    )

    if task is None:
        return None

    return task.model_dump(mode="json")
