"""Popula o banco local com dados de demonstração (idempotente).

Uso: uv run python -m app.seed
"""
from app.core.security import hash_password
from app.database import SessionLocal, init_db
from app.models import Report, ReportCategory, ReportStatus, User, UserRole

DEMO_REPORTS = [
    {
        "title": "Lixo acumulado na esquina da praça",
        "description": "Entulho e sacos de lixo há mais de uma semana na praça.",
        "category": ReportCategory.LIXO,
        "location": "Parque Piauí — Praça Central",
    },
    {
        "title": "Luminária apagada na Rua Principal",
        "description": "Poste queimado em frente ao número 120; trecho escuro à noite.",
        "category": ReportCategory.ILUMINACAO,
        "location": "Parque Piauí — Rua Principal",
    },
    {
        "title": "Bueiro entupido após a chuva",
        "description": "Água acumulada na via; bueiro aparenta obstruído por folhas.",
        "category": ReportCategory.SANEAMENTO,
        "location": "Parque Piauí — Av. Marechal Castelo Branco",
    },
]


def main() -> None:
    init_db()
    with SessionLocal() as db:
        if db.query(Report).count() > 0:
            print("Base já contém denúncias; seed não executado.")
            return
        user = db.query(User).filter_by(email="demo@meubairro.dev").first()
        if user is None:
            user = User(
                name="Usuário de Demonstração",
                email="demo@meubairro.dev",
                password_hash=hash_password("senha-forte-1"),
                role=UserRole.MORADOR,
                neighborhood="Parque Piauí",
            )
            db.add(user)
            db.flush()
        for index, data in enumerate(DEMO_REPORTS):
            status = ReportStatus.ABERTA if index == 0 else ReportStatus.EM_ANALISE
            db.add(
                Report(
                    user_id=user.id,
                    status=status,
                    **data,
                )
            )
        db.commit()
        print(
            "Seed concluído: usuário demo@meubairro.dev"
            f" e {len(DEMO_REPORTS)} denúncias."
        )


if __name__ == "__main__":
    main()
