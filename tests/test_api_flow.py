from __future__ import annotations

from datetime import datetime, timezone


def test_user_can_register_login_and_read_own_profile(api_client) -> None:
    registration = api_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Ana Moradora",
            "email": "ana@example.com",
            "password": "senha-segura-123",
            "neighborhood": "Centro",
        },
    )

    assert registration.status_code == 201
    assert registration.json()["email"] == "ana@example.com"
    assert "password" not in registration.json()

    login = api_client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "password": "senha-segura-123"},
    )

    assert login.status_code == 200
    token = login.json()["access_token"]
    assert login.json()["token_type"] == "bearer"

    profile = api_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert profile.status_code == 200
    assert profile.json()["name"] == "Ana Moradora"
    assert profile.json()["role"] == "MORADOR"


def test_authenticated_resident_can_create_and_filter_reports(api_client) -> None:
    token = api_client.register_and_login(
        name="Bruno Morador",
        email="bruno@example.com",
        password="senha-segura-123",
    )
    headers = {"Authorization": f"Bearer {token}"}

    creation = api_client.post(
        "/api/v1/reports",
        headers=headers,
        json={
            "title": "Lixo acumulado na rua",
            "description": "Há lixo acumulado próximo à praça.",
            "category": "LIXO",
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "location": "Rua Principal, Centro",
            "latitude": -5.0892,
            "longitude": -42.8019,
        },
    )

    assert creation.status_code == 201
    report = creation.json()
    assert report["status"] == "ABERTA"
    assert report["category"] == "LIXO"
    assert report["title"] == "Lixo acumulado na rua"

    mine = api_client.get("/api/v1/reports/mine", headers=headers)
    assert mine.status_code == 200
    assert [item["id"] for item in mine.json()] == [report["id"]]

    filtered = api_client.get("/api/v1/reports?category=LIXO&status=ABERTA")
    assert filtered.status_code == 200
    assert [item["id"] for item in filtered.json()] == [report["id"]]


def test_only_admin_can_update_report_status(api_client, admin_user) -> None:
    resident_token = api_client.register_and_login(
        name="Carla Moradora",
        email="carla@example.com",
        password="senha-segura-123",
    )
    resident_headers = {"Authorization": f"Bearer {resident_token}"}
    creation = api_client.post(
        "/api/v1/reports",
        headers=resident_headers,
        json={
            "title": "Buraco no asfaltamento",
            "description": "Buraco grande na via.",
            "category": "VIAS",
            "location": "Rua das Palmeiras",
        },
    )
    report_id = creation.json()["id"]

    forbidden = api_client.patch(
        f"/api/v1/reports/{report_id}/status",
        headers=resident_headers,
        json={"status": "EM_ANALISE", "comment": "Tentativa indevida."},
    )
    assert forbidden.status_code == 403

    admin_token = api_client.login(admin_user["email"], admin_user["password"])
    updated = api_client.patch(
        f"/api/v1/reports/{report_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "EM_ANALISE", "comment": "Equipe acionada."},
    )

    assert updated.status_code == 200
    assert updated.json()["status"] == "EM_ANALISE"
    assert updated.json()["updated_by"] == admin_user["email"]
