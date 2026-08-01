from fastapi import APIRouter

from app.routers import auth, categories, parties, reports, transactions

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(categories.router)
api_router.include_router(parties.router)
api_router.include_router(transactions.router)
api_router.include_router(reports.router)
