from datetime import datetime, timezone

from backend.memory.models import ConversationMessage
from backend.memory.repository import MemoryRepository


def make_message(
    conversation_id: str,
    role: str,
    content: str,
) -> ConversationMessage:
    return ConversationMessage(
        id=f"{role}-{content}",
        conversation_id=conversation_id,
        role=role,
        content=content,
        timestamp=datetime.now(timezone.utc),
    )


def test_add_and_get_messages():
    repository = MemoryRepository()

    message = make_message("conversation-1", "user", "Hello")

    repository.add_message("conversation-1", message)

    messages = repository.get_messages("conversation-1")

    assert messages == [message]


def test_messages_preserve_order():
    repository = MemoryRepository()

    first = make_message("conversation-1", "user", "First")
    second = make_message("conversation-1", "assistant", "Second")
    third = make_message("conversation-1", "user", "Third")

    repository.add_message("conversation-1", first)
    repository.add_message("conversation-1", second)
    repository.add_message("conversation-1", third)

    messages = repository.get_messages("conversation-1")

    assert messages == [first, second, third]


def test_get_recent_messages():
    repository = MemoryRepository()

    messages = [
        make_message("conversation-1", "user", "First"),
        make_message("conversation-1", "assistant", "Second"),
        make_message("conversation-1", "user", "Third"),
    ]

    for message in messages:
        repository.add_message("conversation-1", message)

    recent = repository.get_recent_messages("conversation-1", 2)

    assert recent == messages[-2:]


def test_conversations_are_isolated():
    repository = MemoryRepository()

    message_one = make_message("conversation-1", "user", "Conversation one")
    message_two = make_message("conversation-2", "user", "Conversation two")

    repository.add_message("conversation-1", message_one)
    repository.add_message("conversation-2", message_two)

    assert repository.get_messages("conversation-1") == [message_one]
    assert repository.get_messages("conversation-2") == [message_two]


def test_nonexistent_conversation_returns_empty_list():
    repository = MemoryRepository()

    assert repository.get_messages("does-not-exist") == []
    assert repository.get_recent_messages("does-not-exist", 5) == []


def test_clear_conversation():
    repository = MemoryRepository()

    message = make_message("conversation-1", "user", "Hello")

    repository.add_message("conversation-1", message)
    repository.clear_conversation("conversation-1")

    assert repository.get_messages("conversation-1") == []


def test_recent_limit_zero_returns_empty():
    repository = MemoryRepository()

    message = make_message("conversation-1", "user", "Hello")
    repository.add_message("conversation-1", message)

    assert repository.get_recent_messages("conversation-1", 0) == []