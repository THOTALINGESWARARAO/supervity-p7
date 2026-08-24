from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.agent.agent import run_agent


router = APIRouter(
    prefix="/agent",
    tags=["agent"],
)


class AgentRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Natural-language request for the HR agent",
    )


@router.post("")
def agent_request(request: AgentRequest):
    """Process a natural-language request using the HR agent."""

    return run_agent(request.message)