from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy.orm import Session

from app.models.source import Source
from app.models.article import Article, ArticleSource
from app.schemas.article import ArticleIn, ArticleSourceIn
from app.core.credibility import compute_credibility
from .rss import parse_rss
from .scrape import scrape_wwe_news, scrape_pwi, scrape_aew
from .normalize import dedup_fingerprint


def _iter_items_for_source(source: Source):
    if source.rss_url:
        for item in parse_rss(source.rss_url):
            yield item
    elif source.base_url and "wwe.com" in (source.base_url or ""):
        for item in scrape_wwe_news(source.base_url):
            yield item
    elif source.base_url and "pwi" in (source.base_url or ""):
        for item in scrape_pwi(source.base_url):
            yield item
    elif source.base_url and "allelitewrestling.com" in (source.base_url or ""):
        for item in scrape_aew(source.base_url):
            yield item


def ingest_once(db: Session, source_ids: Sequence[int] | None = None) -> int:
    sources_q = db.query(Source).filter(Source.is_active == True)
    if source_ids:
        sources_q = sources_q.filter(Source.id.in_(list(source_ids)))
    sources = sources_q.all()

    inserted = 0
    for src in sources:
        for item in _iter_items_for_source(src):
            if not item.get("title") or not item.get("canonical_url"):
                continue
            # Dedup by canonical_url or title fp
            existing = db.query(Article).filter(Article.canonical_url == item["canonical_url"]).first()
            if existing:
                continue
            fp = dedup_fingerprint(item["title"])
            existing2 = db.query(Article).filter(Article.dedup_group_id == fp).first()
            if existing2:
                continue

            article = Article(
                title=item["title"],
                canonical_url=item["canonical_url"],
                content_snippet=item.get("content_snippet"),
                published_at=item.get("published_at"),
                dedup_group_id=fp,
                thumbnail_url=item.get("thumbnail_url"),
            )
            db.add(article)
            db.flush()
            db.add(ArticleSource(article_id=article.id, source_id=src.id, url=item["canonical_url"]))

            # initial credibility
            score, tag = compute_credibility(article.upvotes, article.downvotes, src.source_score)
            article.credibility_score = score
            article.credibility_tag = tag
            inserted += 1

    if inserted:
        try:
            db.commit()
        except Exception as e:
            # Handle database lock gracefully
            db.rollback()
            print(f"Database commit failed: {e}")
            # Try to commit individual articles
            for article in db.new:
                try:
                    db.add(article)
                    db.commit()
                except:
                    db.rollback()
                    continue
    return inserted


