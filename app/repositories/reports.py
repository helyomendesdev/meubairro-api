from sqlalchemy import func, or_, select
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


def _apply_filters(
    statement,
    *,
    user_id: int | None = None,
    category: ReportCategory | None = None,
    status: ReportStatus | None = None,
    query: str | None = None,
):
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
    return statement


def count_reports(
    db: Session,
    *,
    user_id: int | None = None,
    category: ReportCategory | None = None,
    status: ReportStatus | None = None,
    query: str | None = None,
) -> int:
    statement = _apply_filters(
        select(func.count()).select_from(Report),
        user_id=user_id,
        category=category,
        status=status,
        query=query,
    )
    return int(db.scalar(statement) or 0)


def list_reports(
    db: Session,
    *,
    user_id: int | None = None,
    category: ReportCategory | None = None,
    status: ReportStatus | None = None,
    query: str | None = None,
    limit: int | None = None,
    offset: int = 0,
) -> list[Report]:
    statement = _apply_filters(
        select(Report).options(joinedload(Report.reporter)),
        user_id=user_id,
        category=category,
        status=status,
        query=query,
    )
    statement = statement.order_by(Report.created_at.desc())
    if offset:
        statement = statement.offset(offset)
    if limit is not None:
        statement = statement.limit(limit)
    return list(db.scalars(statement).unique().all())
