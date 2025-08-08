from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.models.user import User
from app.schemas.auth import Token, UserCreate, UserOut
from app.core.config import get_settings


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, password_hash=get_password_hash(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)


@router.post("/promote_self", response_model=UserOut)
def promote_self(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """Dev/test convenience: promote the user to admin if not in prod.
    Requires valid credentials; returns 403 in prod.
    """
    settings = get_settings()
    if settings.environment == "prod":
        raise HTTPException(status_code=403, detail="Not allowed in prod")
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user.is_admin:
        user.is_admin = True
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


