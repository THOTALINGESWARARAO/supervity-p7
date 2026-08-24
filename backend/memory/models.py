from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    id: str
    conversation_id: str
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )