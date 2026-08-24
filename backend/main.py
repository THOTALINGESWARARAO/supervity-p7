from fastapi import FastAPI
from pydantic import BaseModel, Field

from backend.agent.routes import router as agent_router
from backend.qa.answer import answer_question
from backend.tasks.routes import router as task_router


app = FastAPI(
    title="HR Knowledge Assistant",
    description="RAG-powered HR question answering API",
    version="1.0.0",
)

app.include_router(task_router)
app.include_router(agent_router)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="HR question to answer",
    )


@app.get("/health")
def health_check():
    """Check whether the API is running."""
    return {"status": "ok"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    """Answer an HR question using the RAG pipeline."""
    return answer_question(request.question)