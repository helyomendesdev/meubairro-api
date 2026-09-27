from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now
from app.models.report import ReportStatus

if TYPE_CHECKING:
    from app.models.report import Report
    from app.models.user import User


class StatusHistory(Base):
    __tablename__ = "status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id"), index=True, nullable=False
    )
    changed_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    previous_status: Mapped[ReportStatus] = mapped_column(
        SqlEnum(ReportStatus), nullable=False
    )
    new_status: Mapped[ReportStatus] = mapped_column(
        SqlEnum(ReportStatus), nullable=False
    )
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    report: Mapped["Report"] = relationship(back_populates="status_history")
    changed_by: Mapped["User"] = relationship(back_populates="status_changes")
