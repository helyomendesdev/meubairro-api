from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import router as api_router
from app.api.v1.health import _health_payload
from app.core.config import get_settings
from app.core.errors import AppError
from app.database import init_db
from app.models import report, status_history, user  # noqa: F401
from app.schemas.health import HealthResponse

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
        headers=headers,
    )


@app.get("/health", response_model=HealthResponse, tags=["health"])
def root_health() -> HealthResponse:
    return _health_payload()


app.include_router(api_router)
