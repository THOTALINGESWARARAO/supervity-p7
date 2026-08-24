from backend.agent.tools import (
    create_task,
    list_tasks,
    search_hr_documents,
    update_task,
)


def test_search_hr_documents():
    results = search_hr_documents(
        "health insurance enrollment",
        top_k=2,
    )

    assert isinstance(results, list)
    assert len(results) <= 2


def test_create_and_list_tasks():
    created = create_task(
        title="Agent-created task",
        description="Created through the agent tool layer",
        priority="high",
    )

    assert created["title"] == "Agent-created task"
    assert created["priority"] == "high"
    assert created["status"] == "todo"

    tasks = list_tasks()

    assert isinstance(tasks, list)
    assert any(
        task["id"] == created["id"]
        for task in tasks
    )


def test_update_task():
    created = create_task(
        title="Task to update",
    )

    updated = update_task(
        task_id=created["id"],
        status="in_progress",
        priority="high",
    )

    assert updated is not None
    assert updated["status"] == "in_progress"
    assert updated["priority"] == "high"