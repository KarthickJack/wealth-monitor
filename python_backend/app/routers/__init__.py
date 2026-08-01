from fastapi import APIRouter

from app.routers import auth, categories, parties

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(categories.router)
api_router.include_router(parties.router)
