from fastapi import APIRouter

from app.api.routes import mushrooms, baskets, utils

api_router = APIRouter()
api_router.include_router(mushrooms.router)
api_router.include_router(baskets.router)
api_router.include_router(utils.router)

