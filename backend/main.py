from fastapi import FastAPI
from pydantic import BaseModel, Field

from backend.agent.routes import router as agent_router
from backend.memory.service import MemoryService
from backend.qa.answer import answer_question
from backend.tasks.routes import router as task_router


app = FastAPI(
    title="HR Knowledge Assistant",
    description="RAG-powered HR question answering API",
    version="1.0.0",
)

app.include_router(task_router)
app.include_router(agent_router)


memory_service = MemoryService()


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="HR question to answer",
    )
    conversation_id: str | None = Field(
        default=None,
        min_length=1,
        description="Optional conversation identifier",
    )


@app.get("/health")
def health_check():
    """Check whether the API is running."""
    return {"status": "ok"}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    """Answer an HR question using RAG and optional conversation memory."""

    conversation_context = ""

    if request.conversation_id:
        messages = memory_service.get_recent_context(
            request.conversation_id,
            limit=10,
        )

        conversation_context = "\n".join(
            f"{message.role.upper()}: {message.content}"
            for message in messages
        )

    result = answer_question(
        question=request.question,
        conversation_context=conversation_context,
    )

    if request.conversation_id:
        memory_service.add_user_message(
            request.conversation_id,
            request.question,
        )

        memory_service.add_assistant_message(
            request.conversation_id,
            result["answer"],
        )

    return result