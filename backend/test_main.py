from fastapi.testclient import TestClient

import backend.main as main_module


client = TestClient(main_module.app)


def mock_answer_question(
    question: str,
    conversation_context: str = "",
) -> dict:
    return {
        "answer": f"Mock answer to: {question}",
        "sources": [
            {
                "source": "test-document.md",
                "chunk_index": 0,
                "score": 0.95,
            }
        ],
    }


def test_ask_without_conversation_id(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "answer_question",
        mock_answer_question,
    )

    response = client.post(
        "/ask",
        json={
            "question": "How many paid leaves do employees get?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "Mock answer to: How many paid leaves do employees get?"
    )
    assert len(data["sources"]) == 1


def test_ask_with_conversation_id_stores_messages(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "answer_question",
        mock_answer_question,
    )

    conversation_id = "test-conversation"

    response = client.post(
        "/ask",
        json={
            "question": "How many paid leaves do employees get?",
            "conversation_id": conversation_id,
        },
    )

    assert response.status_code == 200

    messages = main_module.memory_service.get_conversation(
        conversation_id
    )

    assert len(messages) == 2

    assert messages[0].role == "user"
    assert messages[0].content == (
        "How many paid leaves do employees get?"
    )

    assert messages[1].role == "assistant"
    assert messages[1].content == (
        "Mock answer to: How many paid leaves do employees get?"
    )


def test_second_request_receives_previous_conversation_context(
    monkeypatch,
):
    captured_context = []

    def mock_answer(
        question: str,
        conversation_context: str = "",
    ) -> dict:
        captured_context.append(conversation_context)

        return {
            "answer": f"Mock answer to: {question}",
            "sources": [],
        }

    monkeypatch.setattr(
        main_module,
        "answer_question",
        mock_answer,
    )

    conversation_id = "follow-up-conversation"

    first_response = client.post(
        "/ask",
        json={
            "question": "How many paid leaves do employees get?",
            "conversation_id": conversation_id,
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/ask",
        json={
            "question": "What about sick leave?",
            "conversation_id": conversation_id,
        },
    )

    assert second_response.status_code == 200

    assert len(captured_context) == 2

    assert captured_context[0] == ""

    assert "USER: How many paid leaves do employees get?" in (
        captured_context[1]
    )

    assert (
        "ASSISTANT: Mock answer to: "
        "How many paid leaves do employees get?"
    ) in captured_context[1]


def test_conversations_are_isolated(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "answer_question",
        mock_answer_question,
    )

    conversation_one = "conversation-one"
    conversation_two = "conversation-two"

    response_one = client.post(
        "/ask",
        json={
            "question": "Question from conversation one",
            "conversation_id": conversation_one,
        },
    )

    response_two = client.post(
        "/ask",
        json={
            "question": "Question from conversation two",
            "conversation_id": conversation_two,
        },
    )

    assert response_one.status_code == 200
    assert response_two.status_code == 200

    messages_one = main_module.memory_service.get_conversation(
        conversation_one
    )
    messages_two = main_module.memory_service.get_conversation(
        conversation_two
    )

    assert len(messages_one) == 2
    assert len(messages_two) == 2

    assert all(
        message.conversation_id == conversation_one
        for message in messages_one
    )

    assert all(
        message.conversation_id == conversation_two
        for message in messages_two
    )

    assert "conversation two" not in messages_one[0].content.lower()
    assert "conversation one" not in messages_two[0].content.lower()


def test_new_conversation_has_no_previous_context(monkeypatch):
    captured_context = []

    def mock_answer(
        question: str,
        conversation_context: str = "",
    ) -> dict:
        captured_context.append(conversation_context)

        return {
            "answer": "Mock answer",
            "sources": [],
        }

    monkeypatch.setattr(
        main_module,
        "answer_question",
        mock_answer,
    )

    response = client.post(
        "/ask",
        json={
            "question": "What is the leave policy?",
            "conversation_id": "brand-new-conversation",
        },
    )

    assert response.status_code == 200
    assert captured_context == [""]