from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import threading
import time
import json
import os
from typing import List, Optional, Dict, Any
from sqlalchemy import text
from sqlalchemy.orm import Session

# Import news functionality
from newsite.app.core.database import Base, engine, get_db
from newsite.app.api.auth import router as auth_router
from newsite.app.api.articles import router as articles_router
from newsite.app.api.sources import router as sources_router
from newsite.app.api.votes import router as votes_router
from newsite.app.api.admin import router as admin_router
from newsite.app.api.comments import router as comments_router
from newsite.app.core.config import get_settings
from newsite.app.models.source import Source

# Import stats functionality
from wrestling_api import WrestlingAPI

def create_integrated_app() -> FastAPI:
    app = FastAPI(
        title="Ultimate Wrestling Platform",
        description="Combined wrestling statistics and news platform",
        version="2.0.0"
    )

    # CORS configuration
    settings = get_settings()
    if settings.environment == "prod":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Update this to your specific domain in production
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["*"],
        )
    else:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Create tables for dev/test
    Base.metadata.create_all(bind=engine)

    # Initialize wrestling stats API
    wrestling_api = WrestlingAPI()

    # Include news routers
    app.include_router(auth_router, prefix="/news")
    app.include_router(articles_router, prefix="/news")
    app.include_router(sources_router, prefix="/news")
    app.include_router(votes_router, prefix="/news")
    app.include_router(admin_router, prefix="/news")
    app.include_router(comments_router, prefix="/news")

    # Include stats routers
    app.include_router(create_stats_router(wrestling_api), prefix="/stats")

    # Health check
    @app.get("/health")
    def health():
        return {"status": "ok", "service": "Ultimate Wrestling Platform"}

    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Seed sources for news (non-prod only)
    if settings.environment != "prod":
        seed_news_sources(app)

    return app

def create_stats_router(wrestling_api: WrestlingAPI):
    """Create router for wrestling statistics endpoints"""
    from fastapi import APIRouter
    
    router = APIRouter(tags=["wrestling-stats"])
    
    @router.get("/wrestlers")
    def get_all_wrestlers():
        """Get all wrestlers from the database"""
        try:
            wrestlers = wrestling_api.get_all_wrestlers()
            return {"wrestlers": wrestlers}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/wrestlers/{wrestler_id}")
    def get_wrestler(wrestler_id: str):
        """Get a specific wrestler by ID"""
        try:
            wrestler = wrestling_api.get_wrestler(wrestler_id)
            if not wrestler:
                raise HTTPException(status_code=404, detail="Wrestler not found")
            return wrestler
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/search")
    def search_wrestlers(q: str = Query(..., description="Search query")):
        """Search wrestlers by name or other criteria"""
        try:
            results = wrestling_api.search_wrestlers(q)
            return {
                "query": q,
                "results": results,
                "total_found": len(results),
                "wrestlers": results
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/top-rated")
    def get_top_rated_wrestlers(limit: int = Query(10, le=50)):
        """Get top-rated wrestlers"""
        try:
            wrestlers = wrestling_api.get_top_rated_wrestlers(limit)
            return {
                "wrestlers": [w['wrestler_data'] for w in wrestlers[:limit]],
                "total": len(wrestlers)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/database-stats")
    def get_database_stats():
        """Get database statistics"""
        try:
            stats = wrestling_api.get_database_stats()
            return stats
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/promotions")
    def get_promotions():
        """Get all promotions"""
        try:
            promotions = wrestling_api.get_promotions()
            return {"promotions": promotions}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router

def seed_news_sources(app: FastAPI):
    """Seed news sources for development"""
    from sqlalchemy.orm import Session
    from newsite.app.core.database import SessionLocal

    seed_items = [
        # Tier 1 core
        {"name": "PWInsider", "rss_url": "http://www.pwinsider.com/rss.php", "base_url": "https://www.pwinsider.com"},
        {"name": "Wrestling Observer", "rss_url": "https://www.f4wonline.com/rss.xml", "base_url": "https://www.f4wonline.com"},
        {"name": "Pro Wrestling Torch", "rss_url": "https://www.pwtorch.com/feed", "base_url": "https://www.pwtorch.com"},
        {"name": "Fightful", "rss_url": "https://www.fightful.com/rss.xml", "base_url": "https://www.fightful.com"},
        {"name": "SEScoops", "rss_url": "https://www.sescoops.com/feed", "base_url": "https://www.sescoops.com"},
        {"name": "WrestleZone", "rss_url": "https://www.wrestlezone.com/feed", "base_url": "https://www.wrestlezone.com"},
        {"name": "411Mania Wrestling", "rss_url": "https://411mania.com/wrestling/feed/", "base_url": "https://411mania.com/wrestling/"},
        {"name": "Ringside News", "rss_url": "https://www.ringsidenews.com/feed/", "base_url": "https://www.ringsidenews.com"},
        {"name": "Cageside Seats", "rss_url": "https://www.cagesideseats.com/rss/index.xml", "base_url": "https://www.cagesideseats.com"},

        # Tier 2 official promotions
        {"name": "WWE", "rss_url": None, "base_url": "https://www.wwe.com/news"},
        {"name": "AEW", "rss_url": None, "base_url": "https://www.allelitewrestling.com/aew-news"},
        {"name": "TNA Wrestling", "rss_url": "https://tnawrestling.com/news/feed/", "base_url": "https://tnawrestling.com/news/"},
        {"name": "NJPW", "rss_url": "https://www.njpw1972.com/feed", "base_url": "https://www.njpw1972.com"},
        {"name": "Ring of Honor", "rss_url": "https://www.rohwrestling.com/news/feed", "base_url": "https://www.rohwrestling.com/news"},

        # Tier 3 mainstream sports
        {"name": "ESPN WWE", "rss_url": "https://www.espn.com/espn/rss/wwe/news", "base_url": "https://www.espn.com/wwe/"},
        {"name": "CBS Sports WWE", "rss_url": "https://www.cbssports.com/rss/headlines/wwe/", "base_url": "https://www.cbssports.com/wwe/"},
    ]
    
    db: Session = SessionLocal()
    try:
        for s in seed_items:
            try:
                exists = db.query(Source).filter(Source.name == s["name"]).first()
                if not exists:
                    db.add(Source(name=s["name"], rss_url=s["rss_url"], base_url=s["base_url"], source_score=0.5))
                    db.commit()
            except Exception:
                db.rollback()
                continue
        
        # Disable broken sources
        broken_sources = ["WWE", "AEW", "Fightful"]
        for source_name in broken_sources:
            try:
                source = db.query(Source).filter(Source.name == source_name).first()
                if source and source.is_active:
                    source.is_active = False
                    db.commit()
                    print(f"DISABLED broken source: {source_name}")
            except Exception:
                db.rollback()
                continue
    finally:
        db.close()

    # Start news poller for dev/test
    def _poller(stop_event: threading.Event):
        while not stop_event.is_set():
            try:
                from newsite.app.core.database import SessionLocal as _SessionLocal
                from newsite.app.ingest.ingest import ingest_once as _ingest_once
                _db: Session = _SessionLocal()
                try:
                    _ingest_once(_db)
                finally:
                    _db.close()
            except Exception:
                pass
            stop_event.wait(15 * 60)

    @app.on_event("startup")
    def _start_poller():
        app.state.stop_ingest = threading.Event()
        app.state.ingest_thread = threading.Thread(target=_poller, args=(app.state.stop_ingest,), daemon=True)
        app.state.ingest_thread.start()

    @app.on_event("shutdown")
    def _stop_poller():
        if getattr(app.state, "stop_ingest", None):
            app.state.stop_ingest.set()
        if getattr(app.state, "ingest_thread", None):
            app.state.ingest_thread.join(timeout=5)

# Create the integrated app
app = create_integrated_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
