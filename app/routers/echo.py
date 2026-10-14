from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/echo", tags=["echo"])


class EchoRequest(BaseModel):
    message: str


@router.post("")
def echo(req: EchoRequest):
    return {"echo": req.message}
