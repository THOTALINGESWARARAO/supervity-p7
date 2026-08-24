from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_agent_endpoint():
    response = client.post(
        "/agent",
        json={
            "message": "Show me my tasks."
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["action"] == "list_tasks"
    assert "response" in data
    assert "result" in data