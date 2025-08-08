from pydantic import BaseModel


class VoteIn(BaseModel):
    article_id: int
    direction: str  # 'up' | 'down' | 'clear'


class VoteOut(BaseModel):
    article_id: int
    upvotes: int
    downvotes: int
    credibility_score: float
    credibility_tag: str


