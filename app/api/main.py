from fastapi import APIRouter

from app.api.routes import mushrooms, baskets

api_router = APIRouter()
api_router.include_router(mushrooms.router)
api_router.include_router(baskets.router)

