# MeuBairro API

API back-end do projeto MeuBairro, desenvolvido na disciplina Projeto Integrador II do curso de Tecnologia em Sistemas para Internet da UESPI/UAPI.

Repositório da UI: https://github.com/helyomendesdev/meubairro-ui
Repositório da API: https://github.com/helyomendesdev/meubairro-api

## Estado atual

Implementação funcional da primeira fatia da Entrega 3. O projeto possui:

- aplicação FastAPI executável;
- configuração por variáveis de ambiente;
- CORS para desenvolvimento local;
- persistência SQLAlchemy com SQLite local e PostgreSQL configurável;
- autenticação com senha em Argon2 e tokens JWT;
- cadastro, login e consulta do usuário autenticado;
- criação e consulta de denúncias;
- listagem das próprias denúncias;
- listagem pública com filtros por categoria, status e texto;
- atualização de status restrita ao perfil ADMIN;
- histórico de alterações de status;
- documentação OpenAPI em `/docs` e `/openapi.json`;
- testes automatizados de fluxo completo;
- lint, compilação e CI no GitHub Actions.

## Stack definida para o back-end

- Python 3.12+;
- FastAPI;
- Uvicorn;
- SQLAlchemy 2;
- SQLite para desenvolvimento local;
- PostgreSQL para produção;
- PyJWT para tokens JWT;
- pwdlib com Argon2 para hash de senhas;
- pytest, HTTPX e Ruff;
- uv para ambiente e dependências.

## Endpoints principais

- `GET /health` — saúde da aplicação.
- `GET /api/v1/health` — saúde versionada.
- `POST /api/v1/auth/register` — cadastro de morador.
- `POST /api/v1/auth/login` — autenticação e emissão de JWT.
- `GET /api/v1/auth/me` — perfil do usuário autenticado.
- `POST /api/v1/reports` — criação de denúncia autenticada.
- `GET /api/v1/reports` — consulta pública com filtros.
- `GET /api/v1/reports/mine` — denúncias do usuário autenticado.
- `GET /api/v1/reports/{id}` — detalhamento de denúncia.
- `PATCH /api/v1/reports/{id}/status` — atualização administrativa de status.

Categorias suportadas: `LIXO`, `ILUMINACAO`, `VIAS`, `SANEAMENTO`, `TERRENOS` e `OUTROS`.

Status suportados: `ABERTA`, `EM_ANALISE` e `RESOLVIDA`.

## Estrutura

```text
app/
  api/
    dependencies.py
    v1/
      auth.py
      health.py
      reports.py
      router.py
    router.py
  core/
    config.py
    errors.py
    security.py
  models/
    base.py
    report.py
    status_history.py
    user.py
  repositories/
    reports.py
    users.py
  schemas/
    auth.py
    health.py
    report.py
    user.py
  services/
    auth.py
    reports.py
  database.py
  main.py
tests/
  conftest.py
  test_api_flow.py
  test_health.py
```

## Execução local

Pré-requisitos: Python 3.12+ e uv.

```bash
uv sync --dev
source .venv/bin/activate
uv run uvicorn app.main:app --reload
```

A aplicação ficará disponível em `http://127.0.0.1:8000`.

- Saúde: http://127.0.0.1:8000/health
- Saúde versionada: http://127.0.0.1:8000/api/v1/health
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI: http://127.0.0.1:8000/openapi.json

Para desenvolvimento local, copie `.env.example` para `.env` e ajuste o segredo JWT antes de qualquer uso fora do ambiente local.

## Validação

```bash
uv run ruff check .
uv run python -m compileall -q app tests
uv run pytest -q
```

## Entrega 3 — Projeto Back-End

Artefatos técnicos em andamento:

- stack back-end definida;
- repositório remoto separado da UI;
- API versionada, persistente e integrada ao GitHub;
- fluxo de autenticação e autorização;
- fluxo de criação, consulta, filtro e atualização de denúncias;
- testes automatizados e documentação de execução;
- mínimo de 8 tarefas de API e 8 tarefas de UI registradas no Trello.

A integração completa da UI com a API está sendo implementada no repositório `meubairro-ui`.
