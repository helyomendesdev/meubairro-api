from fastapi import FastAPI

from app.api.router import router as api_router
from app.api.v1.health import _health_payload
from app.core.config import get_settings
from app.schemas.health import HealthResponse

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)


@app.get("/health", response_model=HealthResponse, tags=["health"])
def root_health() -> HealthResponse:
    return _health_payload()


app.include_router(api_router)
