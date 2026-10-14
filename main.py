from fastapi import FastAPI

from app.routers.api import api_router

app = FastAPI(title="Simpo Guide")

app.include_router(api_router)
