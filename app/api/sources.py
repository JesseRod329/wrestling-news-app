from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_admin
from app.models.source import Source
from app.schemas.source import SourceIn, SourceOut


router = APIRouter(prefix="/admin/sources", tags=["sources"])


@router.get("", response_model=list[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return db.query(Source).order_by(Source.name.asc()).all()


@router.post("", response_model=SourceOut)
def create_source(payload: SourceIn, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    existing = db.query(Source).filter(Source.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Source already exists")
    src = Source(
        name=payload.name,
        rss_url=str(payload.rss_url) if payload.rss_url else None,
        base_url=str(payload.base_url) if payload.base_url else None,
        source_score=payload.source_score,
    )
    db.add(src)
    db.commit()
    db.refresh(src)
    return src


