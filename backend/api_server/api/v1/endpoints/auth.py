from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api_server.core.security import create_access_token, get_password_hash, verify_password
from api_server.db.session import get_db
from api_server.models.user import User
from api_server.schemas.auth import Token, UserLogin, UserRegister

router = APIRouter()


@router.post("/register", response_model=Token)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user = User(username=payload.username, password_hash=get_password_hash(payload.password))
    db.add(user)
    db.commit()

    token = create_access_token(subject=user.username)
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.username)
    return Token(access_token=token)


 