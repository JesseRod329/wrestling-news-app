from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.credibility import compute_credibility
from app.dependencies import get_current_user
from app.models.article import Article, ArticleSource
from app.models.source import Source
from app.models.vote import Vote
from app.schemas.vote import VoteIn, VoteOut


router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("", response_model=VoteOut)
def cast_vote(payload: VoteIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    article = db.query(Article).filter(Article.id == payload.article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    vote = db.query(Vote).filter(Vote.article_id == article.id, Vote.user_id == user.id).first()

    if payload.direction == "clear":
        if vote:
            db.delete(vote)
            if vote.is_upvote:
                article.upvotes -= 1
            else:
                article.downvotes -= 1
    elif payload.direction in ("up", "down"):
        is_up = payload.direction == "up"
        if not vote:
            vote = Vote(article_id=article.id, user_id=user.id, is_upvote=is_up)
            db.add(vote)
            if is_up:
                article.upvotes += 1
            else:
                article.downvotes += 1
        else:
            if vote.is_upvote != is_up:
                if is_up:
                    article.upvotes += 1
                    article.downvotes -= 1
                else:
                    article.downvotes += 1
                    article.upvotes -= 1
                vote.is_upvote = is_up
            # else idempotent
    else:
        raise HTTPException(status_code=400, detail="Invalid direction")

    # Recompute credibility based on average source score
    src_ids = [r.source_id for r in db.query(ArticleSource).filter(ArticleSource.article_id == article.id).all()]
    if src_ids:
        sources = db.query(Source).filter(Source.id.in_(src_ids)).all()
        avg_source_score = sum(s.source_score for s in sources) / len(sources)
    else:
        avg_source_score = 0.5
    article.credibility_score, article.credibility_tag = compute_credibility(
        article.upvotes, article.downvotes, avg_source_score
    )

    db.commit()

    return VoteOut(
        article_id=article.id,
        upvotes=article.upvotes,
        downvotes=article.downvotes,
        credibility_score=article.credibility_score,
        credibility_tag=article.credibility_tag,
    )


