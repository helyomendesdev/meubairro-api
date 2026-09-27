from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.report import Report, ReportCategory, ReportStatus
from app.models.status_history import StatusHistory
from app.models.user import User
from app.repositories import reports
from app.schemas.report import ReportCreate, ReportRead, ReportStatusUpdate


def create_report(db: Session, user: User, payload: ReportCreate) -> Report:
    report = Report(
        user_id=user.id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        category=payload.category,
        recorded_at=payload.recorded_at,
        location=payload.location.strip(),
        latitude=payload.latitude,
        longitude=payload.longitude,
        image_url=payload.image_url,
        status=ReportStatus.ABERTA,
    )
    return reports.create(db, report)


def list_reports(
    db: Session,
    *,
    user_id: int | None = None,
    category: ReportCategory | None = None,
    status: ReportStatus | None = None,
    query: str | None = None,
) -> list[Report]:
    return reports.list_reports(
        db,
        user_id=user_id,
        category=category,
        status=status,
        query=query,
    )


def get_report(db: Session, report_id: int) -> Report:
    report = reports.get_by_id(db, report_id)
    if report is None:
        raise NotFoundError("Denúncia não encontrada.")
    return report


def update_status(
    db: Session,
    report_id: int,
    user: User,
    payload: ReportStatusUpdate,
) -> tuple[Report, str]:
    report = get_report(db, report_id)
    previous_status = report.status
    report.status = payload.status
    history = StatusHistory(
        report=report,
        changed_by_id=user.id,
        previous_status=previous_status,
        new_status=payload.status,
        comment=payload.comment.strip() if payload.comment else None,
    )
    db.add(history)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report, user.email


def to_read(report: Report, updated_by: str | None = None) -> ReportRead:
    response = ReportRead.model_validate(report)
    if updated_by is not None:
        response = response.model_copy(update={"updated_by": updated_by})
    return response
