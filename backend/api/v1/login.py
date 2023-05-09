from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api import deps
from core import security
from core.config import settings
from crud.crud_user import crud_user
from schemas.token import Token
router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="账号或密码错误！")
    elif not crud_user.is_active(user):
        raise HTTPException(status_code=400, detail="用户未启用！")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.hashed_password, user.id, expires_delta=access_token_expires,
        ),
        "token_type": "bearer",
    }

