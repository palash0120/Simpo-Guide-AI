from fastapi import APIRouter

from app.routers import agent_chat, chat,  llm_test

api_router = APIRouter(prefix="/api")

api_router.include_router(llm_test.router)
api_router.include_router(chat.router)
api_router.include_router(agent_chat.router)
