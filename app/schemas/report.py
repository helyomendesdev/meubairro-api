from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.report import ReportCategory, ReportStatus


class ReportCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=5, max_length=5000)
    category: ReportCategory
    recorded_at: datetime | None = None
    location: str = Field(min_length=3, max_length=255)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    image_url: str | None = Field(default=None, max_length=500)


class ReportStatusUpdate(BaseModel):
    status: ReportStatus
    comment: str | None = Field(default=None, max_length=2000)


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    description: str
    category: ReportCategory
    status: ReportStatus
    recorded_at: datetime
    location: str
    latitude: float | None
    longitude: float | None
    image_url: str | None
    created_at: datetime
    updated_at: datetime
    updated_by: str | None = None
