from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.constants import API_V1_PREFIX
from app.core.settings import settings
from app.routers import api_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for Wealth Monitor",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=API_V1_PREFIX)


@app.get("/")
def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "Running",
        "docs": "/docs",
        "api": API_V1_PREFIX,
    }


@app.get(f"{API_V1_PREFIX}/health")
def health_check():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "ok",
    }
