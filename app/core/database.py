from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import StaticPool

from .config import get_settings


class Base(DeclarativeBase):
    pass


def _create_engine_from_settings():
    settings = get_settings()
    database_url = settings.get_database_url()
    
    if database_url.startswith("sqlite"):
        # SQLite for dev/test
        return create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool if ":memory:" in database_url else None,
        )
    # PostgreSQL for production
    return create_engine(database_url, pool_pre_ping=True)


engine = _create_engine_from_settings()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


