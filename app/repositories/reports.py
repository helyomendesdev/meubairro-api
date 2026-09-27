from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.models.report import Report, ReportCategory, ReportStatus


def get_by_id(db: Session, report_id: int) -> Report | None:
    statement = (
        select(Report)
        .options(joinedload(Report.reporter))
        .where(Report.id == report_id)
    )
    return db.scalar(statement)


def create(db: Session, report: Report) -> Report:
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def list_reports(
    db: Session,
    *,
    user_id: int | None = None,
    category: ReportCategory | None = None,
    status: ReportStatus | None = None,
    query: str | None = None,
) -> list[Report]:
    statement = select(Report).options(joinedload(Report.reporter))
    if user_id is not None:
        statement = statement.where(Report.user_id == user_id)
    if category is not None:
        statement = statement.where(Report.category == category)
    if status is not None:
        statement = statement.where(Report.status == status)
    if query:
        term = f"%{query.strip()}%"
        statement = statement.where(
            or_(
                Report.title.ilike(term),
                Report.description.ilike(term),
                Report.location.ilike(term),
            )
        )
    statement = statement.order_by(Report.created_at.desc())
    return list(db.scalars(statement).unique().all())
