import random

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/random", tags=["random"])

QUOTES = [
    "Make it work, make it right, make it fast.",
    "Simple is better than complex.",
    "Done is better than perfect.",
    "Talk is cheap. Show me the code.",
]


@router.get("/number")
def random_number(min: int = 1, max: int = 100):
    if min > max:
        raise HTTPException(status_code=400, detail="min must be <= max")
    return {"min": min, "max": max, "number": random.randint(min, max)}


@router.get("/quote")
def random_quote():
    return {"quote": random.choice(QUOTES)}
