from pathlib import Path

from fastapi.testclient import TestClient

from backend.main import app
from backend.tasks.repository import TaskRepository
from backend.tasks.routes import get_task_service
from backend.tasks.service import TaskService


def create_test_service(tmp_path: Path) -> TaskService:
    repository = TaskRepository(tmp_path / "tasks.db")
    return TaskService(repository)


def test_create_get_update_complete_delete_task(tmp_path: Path):
    app.dependency_overrides[get_task_service] = (
        lambda: create_test_service(tmp_path)
    )

    client = TestClient(app)

    try:
        # Create
        create_response = client.post(
            "/tasks",
            json={
                "title": "Complete onboarding",
                "description": "Submit required documents",
                "priority": "high",
            },
        )

        assert create_response.status_code == 201

        created = create_response.json()
        task_id = created["id"]

        assert created["title"] == "Complete onboarding"
        assert created["description"] == "Submit required documents"
        assert created["priority"] == "high"
        assert created["status"] == "todo"

        # Get
        get_response = client.get(f"/tasks/{task_id}")

        assert get_response.status_code == 200
        assert get_response.json()["id"] == task_id

        # Update
        update_response = client.patch(
            f"/tasks/{task_id}",
            json={
                "title": "Complete onboarding - updated",
                "priority": "medium",
            },
        )

        assert update_response.status_code == 200

        updated = update_response.json()

        assert updated["title"] == "Complete onboarding - updated"
        assert updated["priority"] == "medium"
        assert updated["status"] == "todo"

        # Complete
        complete_response = client.post(
            f"/tasks/{task_id}/complete"
        )

        assert complete_response.status_code == 200

        completed = complete_response.json()

        assert completed["id"] == task_id
        assert completed["status"] == "completed"

        # Delete
        delete_response = client.delete(f"/tasks/{task_id}")

        assert delete_response.status_code == 204

        # Verify deletion
        missing_response = client.get(f"/tasks/{task_id}")

        assert missing_response.status_code == 404

    finally:
        app.dependency_overrides.clear()


def test_list_tasks(tmp_path: Path):
    app.dependency_overrides[get_task_service] = (
        lambda: create_test_service(tmp_path)
    )

    client = TestClient(app)

    try:
        client.post(
            "/tasks",
            json={"title": "Task 1"},
        )

        client.post(
            "/tasks",
            json={"title": "Task 2"},
        )

        response = client.get("/tasks")

        assert response.status_code == 200

        tasks = response.json()

        assert len(tasks) == 2

    finally:
        app.dependency_overrides.clear()


def test_get_missing_task():
    client = TestClient(app)

    response = client.get(
        "/tasks/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_create_invalid_task():
    client = TestClient(app)

    response = client.post(
        "/tasks",
        json={"title": ""},
    )

    assert response.status_code == 422


def test_update_missing_task():
    client = TestClient(app)

    response = client.patch(
        "/tasks/00000000-0000-0000-0000-000000000000",
        json={"title": "Updated task"},
    )

    assert response.status_code == 404


def test_complete_missing_task():
    client = TestClient(app)

    response = client.post(
        "/tasks/00000000-0000-0000-0000-000000000000/complete"
    )

    assert response.status_code == 404


def test_delete_missing_task():
    client = TestClient(app)

    response = client.delete(
        "/tasks/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404