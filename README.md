# MeuBairro API

API back-end do projeto MeuBairro, desenvolvido na disciplina Projeto Integrador II do curso de Tecnologia em Sistemas para Internet da UESPI/UAPI.

Repositório da UI: https://github.com/helyomendesdev/meubairro-ui
Repositório da API: https://github.com/helyomendesdev/meubairro-api

## Estado atual

Scaffold inicial da API da Entrega 3. O projeto já possui:

- aplicação FastAPI executável;
- configuração por variáveis de ambiente;
- endpoint de saúde sem versão (`/health`);
- endpoint de saúde versionado (`/api/v1/health`);
- documentação OpenAPI em `/docs` e `/openapi.json`;
- estrutura inicial separando API, schemas, serviços, repositórios, modelos e banco;
- testes automatizados;
- lint, compilação e CI no GitHub Actions.

A implementação dos recursos de usuários e denúncias ainda está pendente.

## Stack definida para o back-end

- Python 3.12+;
- FastAPI;
- Uvicorn;
- SQLAlchemy 2;
- SQLite para desenvolvimento local;
- PostgreSQL para o ambiente de produção;
- PyJWT para tokens JWT;
- pwdlib com Argon2 para hash de senhas;
- pytest, HTTPX e Ruff;
- uv para ambiente e dependências.

A configuração de banco e os recursos de domínio serão adicionados por fatias verticais, com testes antes da implementação.

## Estrutura

```text
app/
  api/
    v1/
      health.py
      router.py
    router.py
  core/
    config.py
  models/
  repositories/
  schemas/
    health.py
  services/
  database.py
  main.py
tests/
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

## Validação

```bash
uv run ruff check .
uv run python -m compileall -q app tests
uv run pytest -q
```

## Entrega 3 — Projeto Back-End

Artefatos em andamento:

- definição da stack back-end;
- repositório remoto no GitHub;
- projeto API local versionado e integrado ao remoto;
- mínimo de 8 tarefas de API no Trello;
- mínimo de 8 tarefas de UI no Trello.

O repositório ainda precisa receber os colaboradores do grupo e a implementação dos recursos previstos nas sprints.
