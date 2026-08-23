import sqlite3
from pathlib import Path
from uuid import UUID

from backend.tasks.models import Task, TaskPriority, TaskStatus


DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "tasks.db"


class TaskRepository:
    def __init__(self, database_path: Path = DATABASE_PATH):
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _initialize_database(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    due_date TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def create(self, task: Task) -> Task:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO tasks (
                    id,
                    title,
                    description,
                    status,
                    priority,
                    due_date,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(task.id),
                    task.title,
                    task.description,
                    task.status.value,
                    task.priority.value,
                    task.due_date.isoformat() if task.due_date else None,
                    task.created_at.isoformat(),
                ),
            )
            connection.commit()

        return task

    def get(self, task_id: UUID) -> Task | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    title,
                    description,
                    status,
                    priority,
                    due_date,
                    created_at
                FROM tasks
                WHERE id = ?
                """,
                (str(task_id),),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_task(row)

    def list_all(self) -> list[Task]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    title,
                    description,
                    status,
                    priority,
                    due_date,
                    created_at
                FROM tasks
                ORDER BY created_at DESC
                """
            ).fetchall()

        return [self._row_to_task(row) for row in rows]

    def delete(self, task_id: UUID) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE id = ?",
                (str(task_id),),
            )
            connection.commit()

        return cursor.rowcount > 0

    @staticmethod
    def _row_to_task(row) -> Task:
        (
            task_id,
            title,
            description,
            status,
            priority,
            due_date,
            created_at,
        ) = row

        return Task(
            id=UUID(task_id),
            title=title,
            description=description,
            status=TaskStatus(status),
            priority=TaskPriority(priority),
            due_date=(
                None
                if due_date is None
                else __import__("datetime").datetime.fromisoformat(due_date)
            ),
            created_at=__import__("datetime").datetime.fromisoformat(created_at),
        )

    def update(self, task: Task) -> Task:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE tasks
                SET
                    title = ?,
                    description = ?,
                    status = ?,
                    priority = ?,
                    due_date = ?
                WHERE id = ?
                """,
                (
                    task.title,
                    task.description,
                    task.status.value,
                    task.priority.value,
                    task.due_date.isoformat() if task.due_date else None,
                    str(task.id),
                ),
            )

        return task