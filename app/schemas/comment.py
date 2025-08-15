from datetime import datetime
from pydantic import BaseModel


class CommentIn(BaseModel):
    body: str


class CommentOut(BaseModel):
    id: int
    article_id: int
    user_id: int
    body: str
    created_at: datetime

    class Config:
        from_attributes = True


