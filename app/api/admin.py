from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_admin
from app.ingest.ingest import ingest_once


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/ingest")
def run_ingest(_=Depends(require_admin), db: Session = Depends(get_db)):
    inserted = ingest_once(db)
    return {"inserted": inserted}


