from fastapi import APIRouter

from app.routers import echo, health, llm_test, random_api

api_router = APIRouter(prefix="/api")

api_router.include_router(health.router)
api_router.include_router(random_api.router)
api_router.include_router(echo.router)
api_router.include_router(llm_test.router)
