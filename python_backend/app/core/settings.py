from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings
    Loaded automatically from .env
    """

    # ==========================================
    # Application
    # ==========================================

    app_name: str
    app_version: str
    debug: bool = True

    # ==========================================
    # Database
    # ==========================================

    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str

    # ==========================================
    # JWT
    # ==========================================

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int

    # ==========================================
    # Pydantic Settings
    # ==========================================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a singleton Settings instance.
    """
    return Settings()


settings = get_settings()