from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter()


def _health_payload() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service="meubairro-api",
        version=settings.app_version,
    )


@router.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    return _health_payload()
