from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agent import run

router = APIRouter(prefix="/agent", tags=["agent"])


class AgentRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class AgentResponse(BaseModel):
    answer: str
    trace: list[dict]


@router.post("/chat", response_model=AgentResponse)
def agent_chat(req: AgentRequest):
    try:
        return run(req.message)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Agent failed: {type(e).__name__}")
