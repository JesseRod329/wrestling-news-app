from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import threading
import time
from sqlalchemy import text

from app.core.database import Base, engine
from app.api.auth import router as auth_router
from app.api.articles import router as articles_router
from app.api.sources import router as sources_router
from app.api.votes import router as votes_router
from app.api.admin import router as admin_router
from app.api.comments import router as comments_router
from app.core.config import get_settings
from app.models.source import Source


def create_app() -> FastAPI:
    app = FastAPI(title="Real Wrestling News")

    # CORS configuration
    settings = get_settings()
    if settings.environment == "prod":
        # In production, be more restrictive with CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Update this to your specific domain in production
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["*"],
        )
    else:
        # In development, allow all origins
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Create tables for dev/test. In prod use Alembic migrations.
    Base.metadata.create_all(bind=engine)

    # Lightweight migration for SQLite dev: add columns if missing
    try:
        if engine.dialect.name == "sqlite":
            with engine.connect() as conn:
                # Ensure articles.thumbnail_url exists
                res = conn.exec_driver_sql("PRAGMA table_info(articles)")
                cols = {row[1] for row in res.fetchall()}  # row[1] is column name
                if "thumbnail_url" not in cols:
                    conn.exec_driver_sql("ALTER TABLE articles ADD COLUMN thumbnail_url VARCHAR(1000)")
                
                # Ensure sources.is_active exists
                res = conn.exec_driver_sql("PRAGMA table_info(sources)")
                cols = {row[1] for row in res.fetchall()}  # row[1] is column name
                if "is_active" not in cols:
                    conn.exec_driver_sql("ALTER TABLE sources ADD COLUMN is_active BOOLEAN DEFAULT 1 NOT NULL")
                    conn.commit()
    except Exception:
        # Best-effort; avoid startup failure in dev
        pass

    app.include_router(auth_router)
    app.include_router(articles_router)
    app.include_router(sources_router)
    app.include_router(votes_router)
    app.include_router(admin_router)
    app.include_router(comments_router)

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Seed sources in non-prod for convenience
    settings = get_settings()
    if settings.environment != "prod":
        from sqlalchemy.orm import Session
        from app.core.database import SessionLocal

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
            # Fox Sports requires partner key for optimized RSS; skip for now to avoid breakage
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
                    # Handle race condition gracefully
                    db.rollback()
                    continue
            
            # CRITICAL: Disable broken sources that are polluting the feed
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

        # Lightweight in-process poller for dev/test only
        def _poller(stop_event: threading.Event):
            while not stop_event.is_set():
                try:
                    from app.core.database import SessionLocal as _SessionLocal
                    from app.ingest.ingest import ingest_once as _ingest_once
                    _db: Session = _SessionLocal()
                    try:
                        _ingest_once(_db)
                    finally:
                        _db.close()
                except Exception:
                    # Best-effort; avoid crashing dev server
                    pass
                # Sleep ~15 minutes or until stop requested
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

    return app


app = create_app()


