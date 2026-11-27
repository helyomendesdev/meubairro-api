"""Testes das tarefas da Entrega 4 do projeto API (stats, paginação, ETag,
mensagens 401, senha forte, erros de validação uniformes)."""


def test_password_fraca_sem_numero_rejeitada(api_client):
    resposta = api_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Usuário Teste",
            "email": "e4api@test.com",
            "password": "senhaforte",
            "neighborhood": "Parque Piauí",
        },
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["detail"] == "Dados inválidos."
    campos = {campo["field"] for campo in corpo["fields"]}
    assert "password" in campos
    assert any("número" in campo["message"] for campo in corpo["fields"])


def test_422_uniforme_em_denuncia_invalida(api_client):
    token = api_client.register_and_login(
        name="E4 Invalida",
        email="e4-invalida@test.com",
        password="senha-forte-1",
    )
    resposta = api_client.post(
        "/api/v1/reports",
        json={"title": "x", "description": "y", "category": "LIXO", "location": "z"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert set(corpo) == {"detail", "error", "fields"}
    assert corpo["fields"][0]["field"] in {"title", "description", "location"}


def test_token_invalido_mensagem_especifica(api_client):
    resposta = api_client.get(
        "/api/v1/reports/mine", headers={"Authorization": "Bearer token-quebrado"}
    )
    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Token inválido ou expirado."


def test_stats_agregacoes(api_client):
    token = api_client.register_and_login(
        name="E4 Stats",
        email="e4-stats@test.com",
        password="senha-forte-1",
    )
    api_client.post(
        "/api/v1/reports",
        json={
            "title": "Buraco na via",
            "description": "Asfalto danificado no meio da rua.",
            "category": "VIAS",
            "location": "Rua das Palmeiras, 10",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    resposta = api_client.get("/api/v1/reports/stats")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["total"] >= 1
    assert all(item["count"] >= 1 for item in corpo["by_status"])
    categorias = {item["category"] for item in corpo["by_category"]}
    assert "VIAS" in categorias


def test_paginacao_e_total(api_client):
    token = api_client.register_and_login(
        name="E4 Paginacao",
        email="e4-paginacao@test.com",
        password="senha-forte-1",
    )
    for indice in range(3):
        api_client.post(
            "/api/v1/reports",
            json={
                "title": f"Ocorrência de teste {indice}",
                "description": "Descrição suficiente para o teste.",
                "category": "OUTROS",
                "location": "Rua de teste",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    resposta = api_client.get("/api/v1/reports?limit=2&offset=0")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2
    assert int(resposta.headers["X-Total-Count"]) >= 3
    pagina2 = api_client.get("/api/v1/reports?limit=2&offset=2")
    ids1 = {item["id"] for item in resposta.json()}
    ids2 = {item["id"] for item in pagina2.json()}
    assert ids1.isdisjoint(ids2)


def test_etag_304_quando_conteudo_igual(api_client):
    primeira = api_client.get("/api/v1/reports")
    assert primeira.status_code == 200
    etag = primeira.headers["ETag"]
    segunda = api_client.get("/api/v1/reports", headers={"If-None-Match": etag})
    assert segunda.status_code == 304
    assert segunda.headers["ETag"] == etag
