from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_roles
from app.database import get_db
from app.models.report import ReportCategory, ReportStatus
from app.models.user import User, UserRole
from app.schemas.report import ReportCreate, ReportRead, ReportStatusUpdate
from app.services import reports

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def create_report(
    payload: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReportRead:
    return reports.to_read(reports.create_report(db, current_user, payload))


@router.get("/mine", response_model=list[ReportRead])
def list_my_reports(
    category: ReportCategory | None = None,
    status: ReportStatus | None = None,
    query: str | None = Query(default=None, max_length=120),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ReportRead]:
    items = reports.list_reports(
        db,
        user_id=current_user.id,
        category=category,
        status=status,
        query=query,
    )
    return [reports.to_read(item) for item in items]


@router.get("", response_model=list[ReportRead])
def list_public_reports(
    category: ReportCategory | None = None,
    status: ReportStatus | None = None,
    query: str | None = Query(default=None, max_length=120),
    db: Session = Depends(get_db),
) -> list[ReportRead]:
    items = reports.list_reports(db, category=category, status=status, query=query)
    return [reports.to_read(item) for item in items]


@router.get("/{report_id}", response_model=ReportRead)
def get_report(report_id: int, db: Session = Depends(get_db)) -> ReportRead:
    return reports.to_read(reports.get_report(db, report_id))


@router.patch("/{report_id}/status", response_model=ReportRead)
def update_report_status(
    report_id: int,
    payload: ReportStatusUpdate,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> ReportRead:
    report, updated_by = reports.update_status(db, report_id, current_user, payload)
    return reports.to_read(report, updated_by=updated_by)
