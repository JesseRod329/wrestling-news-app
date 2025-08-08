from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.core.database import get_db
from app.core.credibility import compute_credibility
from app.dependencies import get_current_user
from app.models.article import Article, ArticleSource
from app.models.source import Source
from app.schemas.article import ArticleIn, ArticleOut


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=list[dict])
def list_articles(
    db: Session = Depends(get_db),
    tag: str | None = Query(default=None),
    source_id: int | None = Query(default=None),
    q: str | None = Query(default=None),
    sort: str | None = Query(default=None),
    limit: int = Query(default=50, le=100),
):
    query_ = db.query(Article)
    if tag and tag.lower() not in {"undefined", "null", "none", ""}:
        query_ = query_.filter(Article.credibility_tag == tag)
    if source_id:
        query_ = query_.join(ArticleSource).filter(ArticleSource.source_id == source_id)
    if q:
        term = f"%{q.strip()}%"
        query_ = query_.filter(or_(Article.title.ilike(term), Article.content_snippet.ilike(term)))
    # Sorting
    if sort == "top_week":
        one_week_ago = func.datetime(func.current_timestamp(), "-7 days")
        query_ = query_.filter(Article.created_at >= one_week_ago).order_by((Article.upvotes - Article.downvotes).desc())
    elif sort == "top_all":
        query_ = query_.order_by((Article.upvotes - Article.downvotes).desc(), Article.created_at.desc())
    else:
        query_ = query_.order_by(Article.created_at.desc())
    query_ = query_.limit(limit)
    
    articles = query_.all()
    result = []
    for article in articles:
        # Get source information
        source_info = db.query(Source).join(ArticleSource).filter(ArticleSource.article_id == article.id).first()
        article_dict = {
            "id": article.id,
            "title": article.title,
            "canonical_url": article.canonical_url,
            "content_snippet": article.content_snippet,
            "thumbnail_url": article.thumbnail_url,
            "published_at": article.published_at,
            "upvotes": article.upvotes,
            "downvotes": article.downvotes,
            "credibility_score": article.credibility_score,
            "credibility_tag": article.credibility_tag,
            "created_at": article.created_at,
            "source_name": source_info.name if source_info else "Unknown",
            "source_id": source_info.id if source_info else None,
        }
        result.append(article_dict)
    
    return result


@router.get("/{article_id}", response_model=ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    art = db.query(Article).filter(Article.id == article_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Article not found")
    return art


@router.post("", response_model=ArticleOut)
def create_article(
    payload: ArticleIn,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    existing = db.query(Article).filter(Article.canonical_url == str(payload.canonical_url)).first()
    if existing:
        return existing

    article = Article(
        title=payload.title,
        canonical_url=str(payload.canonical_url),
        content_snippet=payload.content_snippet,
        published_at=payload.published_at,
        thumbnail_url=str(payload.thumbnail_url) if payload.thumbnail_url else None,
    )
    db.add(article)
    db.flush()

    for s in payload.sources:
        src = db.query(Source).filter(Source.id == s.source_id).first()
        if not src:
            raise HTTPException(status_code=400, detail=f"Source {s.source_id} not found")
        db.add(ArticleSource(article_id=article.id, source_id=src.id, url=str(s.url)))

    # Compute initial credibility using avg source score
    if payload.sources:
        avg_source_score = sum(
            db.query(Source).filter(Source.id == s.source_id).first().source_score for s in payload.sources
        ) / len(payload.sources)
    else:
        avg_source_score = 0.5
    score, tag = compute_credibility(article.upvotes, article.downvotes, avg_source_score)
    article.credibility_score = score
    article.credibility_tag = tag

    db.commit()
    db.refresh(article)
    return article


