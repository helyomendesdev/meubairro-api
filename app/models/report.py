from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now

if TYPE_CHECKING:
    from app.models.status_history import StatusHistory
    from app.models.user import User


class ReportStatus(str, Enum):
    ABERTA = "ABERTA"
    EM_ANALISE = "EM_ANALISE"
    RESOLVIDA = "RESOLVIDA"


class ReportCategory(str, Enum):
    LIXO = "LIXO"
    ILUMINACAO = "ILUMINACAO"
    VIAS = "VIAS"
    SANEAMENTO = "SANEAMENTO"
    TERRENOS = "TERRENOS"
    OUTROS = "OUTROS"


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[ReportCategory] = mapped_column(
        SqlEnum(ReportCategory), index=True, nullable=False
    )
    status: Mapped[ReportStatus] = mapped_column(
        SqlEnum(ReportStatus), default=ReportStatus.ABERTA, index=True, nullable=False
    )
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    reporter: Mapped["User"] = relationship(back_populates="reports")
    status_history: Mapped[list["StatusHistory"]] = relationship(
        back_populates="report",
        cascade="all, delete-orphan",
        order_by="StatusHistory.changed_at",
    )
