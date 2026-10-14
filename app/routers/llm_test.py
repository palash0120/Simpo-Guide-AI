from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.llm import get_llm

router = APIRouter(prefix="/llm", tags=["llm"])


class LLMTestRequest(BaseModel):
    prompt: str


@router.post("/test")
def llm_test(req: LLMTestRequest):
    try:
        response = get_llm().invoke(req.prompt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {type(e).__name__}")
    return {"reply": response.content}
