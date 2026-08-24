import uuid

from backend.memory.models import ConversationMessage
from backend.memory.repository import MemoryRepository


class MemoryService:
    def __init__(self, repository: MemoryRepository | None = None) -> None:
        self.repository = repository or MemoryRepository()

    def _validate_input(self, conversation_id: str, content: str) -> None:
        if not conversation_id or not conversation_id.strip():
            raise ValueError("conversation_id cannot be blank")

        if not content or not content.strip():
            raise ValueError("content cannot be blank")

    def _add_message(
        self,
        conversation_id: str,
        content: str,
        role: str,
    ) -> ConversationMessage:
        self._validate_input(conversation_id, content)

        message = ConversationMessage(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        return self.repository.add_message(conversation_id, message)

    def add_user_message(
        self,
        conversation_id: str,
        content: str,
    ) -> ConversationMessage:
        return self._add_message(conversation_id, content, "user")

    def add_assistant_message(
        self,
        conversation_id: str,
        content: str,
    ) -> ConversationMessage:
        return self._add_message(conversation_id, content, "assistant")

    def get_conversation(
        self,
        conversation_id: str,
    ) -> list[ConversationMessage]:
        return self.repository.get_messages(conversation_id)

    def get_recent_context(
        self,
        conversation_id: str,
        limit: int = 10,
    ) -> list[ConversationMessage]:
        return self.repository.get_recent_messages(
            conversation_id,
            limit,
        )

    def clear_conversation(self, conversation_id: str) -> None:
        self.repository.clear_conversation(conversation_id)