from __future__ import annotations

import asyncio
from collections.abc import Generator
from typing import Any

import httpx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import User, UserRole
from app.services.auth import hash_password


class ApiClient:
    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        async def send() -> httpx.Response:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://test",
            ) as client:
                return await client.request(method, path, **kwargs)

        return asyncio.run(send())

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        return self._request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> httpx.Response:
        return self._request("PATCH", path, **kwargs)

    def register_and_login(self, *, name: str, email: str, password: str) -> str:
        registration = self.post(
            "/api/v1/auth/register",
            json={
                "name": name,
                "email": email,
                "password": password,
                "neighborhood": "Centro",
            },
        )
        assert registration.status_code == 201, registration.text
        return self.login(email, password)

    def login(self, email: str, password: str) -> str:
        response = self.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        assert response.status_code == 200, response.text
        return response.json()["access_token"]


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db() -> Generator[Session, None, None]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with session_factory() as session:
        yield session
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def api_client(db_session: Session) -> ApiClient:
    return ApiClient()


@pytest.fixture
def admin_user(db_session: Session) -> dict[str, str]:
    user = User(
        name="Administrador",
        email="admin@example.com",
        password_hash=hash_password("admin-pass-123"),
        role=UserRole.ADMIN,
        neighborhood="Centro",
    )
    db_session.add(user)
    db_session.commit()
    return {"email": user.email, "password": "admin-pass-123"}
