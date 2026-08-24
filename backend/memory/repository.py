from backend.memory.models import ConversationMessage


class MemoryRepository:
    def __init__(self) -> None:
        self._messages: dict[str, list[ConversationMessage]] = {}

    def add_message(
        self,
        conversation_id: str,
        message: ConversationMessage,
    ) -> ConversationMessage:
        self._messages.setdefault(conversation_id, []).append(message)
        return message

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[ConversationMessage]:
        return list(self._messages.get(conversation_id, []))

    def get_recent_messages(
        self,
        conversation_id: str,
        limit: int,
    ) -> list[ConversationMessage]:
        if limit <= 0:
            return []

        messages = self._messages.get(conversation_id, [])
        return list(messages[-limit:])

    def clear_conversation(self, conversation_id: str) -> None:
        self._messages.pop(conversation_id, None)