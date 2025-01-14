from fastapi import FastAPI
from app.api.main import api_router


PROJECT_NAME = 'Mushrooms and baskets'

app = FastAPI(
    title=PROJECT_NAME,
    openapi_url="/openapi.json",
)

app.include_router(api_router, prefix='/api')
