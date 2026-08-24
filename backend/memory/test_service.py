import pytest

from backend.memory.repository import MemoryRepository
from backend.memory.service import MemoryService


@pytest.fixture
def service() -> MemoryService:
    return MemoryService(MemoryRepository())


def test_add_user_message(service: MemoryService):
    message = service.add_user_message(
        "conversation-1",
        "How many paid leaves do I get?",
    )

    assert message.conversation_id == "conversation-1"
    assert message.role == "user"
    assert message.content == "How many paid leaves do I get?"
    assert message.id


def test_add_assistant_message(service: MemoryService):
    message = service.add_assistant_message(
        "conversation-1",
        "Employees receive 18 paid leaves per year.",
    )

    assert message.conversation_id == "conversation-1"
    assert message.role == "assistant"
    assert message.content == "Employees receive 18 paid leaves per year."
    assert message.id


def test_messages_are_stored_in_order(service: MemoryService):
    user_message = service.add_user_message(
        "conversation-1",
        "First question",
    )
    assistant_message = service.add_assistant_message(
        "conversation-1",
        "First answer",
    )
    second_user_message = service.add_user_message(
        "conversation-1",
        "Second question",
    )

    messages = service.get_conversation("conversation-1")

    assert messages == [
        user_message,
        assistant_message,
        second_user_message,
    ]


def test_recent_context_respects_limit(service: MemoryService):
    messages = []

    for index in range(5):
        messages.append(
            service.add_user_message(
                "conversation-1",
                f"Message {index}",
            )
        )

    recent = service.get_recent_context("conversation-1", limit=2)

    assert recent == messages[-2:]


def test_conversations_are_isolated(service: MemoryService):
    message_one = service.add_user_message(
        "conversation-1",
        "Conversation one",
    )
    message_two = service.add_user_message(
        "conversation-2",
        "Conversation two",
    )

    assert service.get_conversation("conversation-1") == [message_one]
    assert service.get_conversation("conversation-2") == [message_two]


def test_blank_conversation_id_is_rejected(service: MemoryService):
    with pytest.raises(ValueError, match="conversation_id cannot be blank"):
        service.add_user_message("", "Hello")


def test_whitespace_conversation_id_is_rejected(service: MemoryService):
    with pytest.raises(ValueError, match="conversation_id cannot be blank"):
        service.add_user_message("   ", "Hello")


def test_blank_content_is_rejected(service: MemoryService):
    with pytest.raises(ValueError, match="content cannot be blank"):
        service.add_user_message("conversation-1", "")


def test_whitespace_content_is_rejected(service: MemoryService):
    with pytest.raises(ValueError, match="content cannot be blank"):
        service.add_user_message("conversation-1", "   ")


def test_clear_conversation(service: MemoryService):
    service.add_user_message(
        "conversation-1",
        "Hello",
    )

    service.clear_conversation("conversation-1")

    assert service.get_conversation("conversation-1") == []