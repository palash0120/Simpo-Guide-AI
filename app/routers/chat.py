from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag import answer

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


@router.post("")
def chat(req: ChatRequest):
    try:
        return answer(req.message)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Chat failed: {type(e).__name__}")
