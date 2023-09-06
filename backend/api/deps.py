from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import security
from core.config import settings
from core.security import verify_password, get_password_hash
from crud.crud_user import crud_user
from models.user_model import UserModel
from schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def login_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> UserModel:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无法验证凭据！",
        )
    user = crud_user.get(db, unique_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="找不到该用户！")
    if not verify_password(user.hashed_password, token_data.check):
        raise HTTPException(status_code=400, detail="token已失效，请重新登录！")
    return user


def active_user(
    current_user: UserModel = Depends(login_user),
) -> UserModel:
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="该用户未启用！")
    return current_user


def super_user(
    current_user: UserModel = Depends(login_user),
) -> UserModel:
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="该用户权限不够！"
        )
    return current_user
