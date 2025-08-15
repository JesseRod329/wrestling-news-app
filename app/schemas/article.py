from datetime import datetime
from pydantic import BaseModel, HttpUrl


class ArticleSourceIn(BaseModel):
    source_id: int
    url: HttpUrl


class ArticleIn(BaseModel):
    title: str
    canonical_url: HttpUrl
    content_snippet: str | None = None
    published_at: datetime | None = None
    sources: list[ArticleSourceIn] = []
    thumbnail_url: HttpUrl | None = None


class ArticleOut(BaseModel):
    id: int
    title: str
    canonical_url: str
    content_snippet: str | None
    thumbnail_url: str | None
    published_at: datetime | None
    upvotes: int
    downvotes: int
    credibility_score: float
    credibility_tag: str
    created_at: datetime

    class Config:
        from_attributes = True


