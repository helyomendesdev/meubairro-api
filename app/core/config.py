from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MeuBairro API"
    app_description: str = "API back-end do projeto MeuBairro."
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./meubairro.db"
    jwt_secret: str = "dev-only-change-this-secret-meubairro"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(
        env_prefix="MEUBAIRRO_",
        env_file=".env",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    @field_validator("access_token_expire_minutes")
    @classmethod
    def validate_expiration(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("A expiração do token deve ser positiva.")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
