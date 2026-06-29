from fastapi import FastAPI

from app.core.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for Wealth Monitor"
)


@app.get("/")
def health_check():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "Running"
    }