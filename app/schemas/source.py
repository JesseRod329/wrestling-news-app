from datetime import datetime
from pydantic import BaseModel, HttpUrl


class SourceIn(BaseModel):
    name: str
    rss_url: HttpUrl | None = None
    base_url: HttpUrl | None = None
    source_score: float = 0.5


class SourceOut(BaseModel):
    id: int
    name: str
    rss_url: str | None
    base_url: str | None
    source_score: float
    created_at: datetime

    class Config:
        from_attributes = True


