import hashlib
import json

from fastapi import APIRouter, Depends, Header, Query, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_roles
from app.database import get_db
from app.models.report import ReportCategory, ReportStatus
from app.models.user import User, UserRole
from app.schemas.report import ReportCreate, ReportRead, ReportStats, ReportStatusUpdate
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


@router.get(
    "",
    response_model=list[ReportRead],
    summary="Listagem pública com filtros, paginação e ETag.",
)
def list_public_reports(
    response: Response,
    category: ReportCategory | None = None,
    status: ReportStatus | None = None,
    query: str | None = Query(default=None, max_length=120),
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    if_none_match: str | None = Header(default=None, alias="If-None-Match"),
    db: Session = Depends(get_db),
) -> list[ReportRead] | Response:
    total = reports.count_reports(db, category=category, status=status, query=query)
    items = reports.list_reports(
        db, category=category, status=status, query=query, limit=limit, offset=offset
    )
    payload = [reports.to_read(item).model_dump(mode="json") for item in items]
    etag = '"%s"' % hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    response.headers["X-Total-Count"] = str(total)
    response.headers["ETag"] = etag
    if if_none_match is not None:
        candidates = {tag.strip() for tag in if_none_match.split(",")}
        candidates |= {tag[2:] for tag in candidates if tag.startswith("W/")}
        if etag in candidates or "*" in candidates:
            return Response(status_code=304, headers={"ETag": etag})
    return [reports.to_read(item) for item in items]


@router.get(
    "/stats",
    summary="Agregações de denúncias por status e categoria.",
)
def report_stats(db: Session = Depends(get_db)) -> ReportStats:
    return reports.stats(db)


@router.get(
    "/{report_id}",
    responses={
        404: {
            "description": "Denúncia não encontrada.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Denúncia não encontrada.",
                        "error": "Denúncia não encontrada.",
                    }
                }
            },
        }
    },
)
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
