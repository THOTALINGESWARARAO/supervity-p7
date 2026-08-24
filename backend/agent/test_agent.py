from backend.agent.agent import HRAgent


def test_agent_can_answer_hr_question():
    agent = HRAgent()

    result = agent.run(
        "What does the HR knowledge base say about health insurance enrollment?"
    )

    assert result["action"] == "search_hr_documents"
    assert isinstance(result["result"], list)
    assert result["response"]


def test_agent_can_create_task():
    agent = HRAgent()

    result = agent.run(
        "Create a high priority task called "
        "'Submit onboarding documents'."
    )

    assert result["action"] == "create_task"
    assert result["result"]["title"] == (
        "Submit onboarding documents"
    )
    assert result["result"]["priority"] == "high"
    assert result["response"]


def test_agent_can_list_tasks():
    agent = HRAgent()

    result = agent.run(
        "Show me my tasks."
    )

    assert result["action"] == "list_tasks"
    assert isinstance(result["result"], list)
    assert result["response"]