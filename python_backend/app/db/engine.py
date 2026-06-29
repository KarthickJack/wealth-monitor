from sqlalchemy import create_engine

from app.core.config import DATABASE_URL
from app.core.settings import settings


engine = create_engine(
    DATABASE_URL,
    echo=True,
    echo=settings.debug,
    pool_pre_ping=True
)