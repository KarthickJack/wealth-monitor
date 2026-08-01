from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment / .env
    """

    app_name: str = "Wealth Monitor"
    app_version: str = "1.0.0"
    debug: bool = True

    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "wealth_monitor"
    database_user: str = "postgres"
    database_password: str = "postgres"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24

    # Comma-separated list in .env, e.g. http://localhost:5173,http://localhost:3000
    cors_origins_raw: str = "http://localhost:5173,http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
