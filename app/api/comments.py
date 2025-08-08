from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.comment import Comment
from app.models.article import Article
from app.schemas.comment import CommentIn, CommentOut


router = APIRouter(prefix="/articles/{article_id}/comments", tags=["comments"])


@router.get("", response_model=list[CommentOut])
def list_comments(article_id: int, db: Session = Depends(get_db)):
    exists = db.query(Article.id).filter(Article.id == article_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Article not found")
    return db.query(Comment).filter(Comment.article_id == article_id).order_by(Comment.created_at.asc()).all()


@router.post("", response_model=CommentOut)
def add_comment(article_id: int, payload: CommentIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    exists = db.query(Article.id).filter(Article.id == article_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Article not found")
    c = Comment(article_id=article_id, user_id=user.id, body=payload.body.strip())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


