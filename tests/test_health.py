import asyncio

import httpx

from app.main import app


def get(path: str) -> httpx.Response:
    async def request() -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            return await client.get(path)

    return asyncio.run(request())


def test_health_endpoint_reports_service_status() -> None:
    response = get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "meubairro-api",
        "version": "0.1.0",
    }


def test_versioned_health_endpoint_is_available() -> None:
    response = get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "meubairro-api"
    assert response.json()["version"] == "0.1.0"


def test_openapi_identifies_the_api() -> None:
    response = get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"] == {
        "title": "MeuBairro API",
        "description": "API back-end do projeto MeuBairro.",
        "version": "0.1.0",
    }
