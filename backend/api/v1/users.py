from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from api import deps
from core.security import get_password_hash, verify_password
from crud.crud_user import crud_user
from models.user_model import UserModel
from schemas.msg import Msg
from schemas.user import User, UserUpdate, UserCreate

router = APIRouter()


@router.get("/", response_model=List[User])
def get_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(deps.super_user),
) -> Any:
    """
    获取用户列表
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    old_password: str = Body(None),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    修改当前登陆用户信息
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        if old_password is None:
            raise HTTPException(status_code=400, detail="修改密码必须输入旧密码！")
        if not verify_password(old_password, crud_user.get(db, current_user.id).hashed_password):
            raise HTTPException(status_code=400, detail="旧密码错误！")
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=User)
def read_user_me(
    current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取当前用户信息
    """
    return current_user


@router.get("/{user_id}", response_model=User)
def read_user_by_id(
    user_id: int,
    current_user: UserModel = Depends(deps.active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    通过id获取用户信息
    """
    user = crud_user.get(db, unique_id=user_id)
    if user == current_user:
        return user
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="该用户权限不足！"
        )
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: UserModel = Depends(deps.super_user),
) -> Any:
    """
    修改用户信息
    """
    user = crud_user.get(db, unique_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="找不到该用户！",
        )
    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=User)
def delete_user_by_id(
    user_id: int,
    current_user: UserModel = Depends(deps.super_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    删除用户
    """
    user = crud_user.get(db, unique_id=Msg)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="找不到该用户！",
        )
    if user == current_user:
        raise HTTPException(
            status_code=400, detail="不能删除自己！"
        )
    crud_user.remove(db, user_id)
    return Msg(msg='删除成功！')


@router.post("/", response_model=User)
def create_user(user_in: UserCreate,
                db: Session = Depends(deps.get_db),
                current_user: UserModel = Depends(deps.super_user)
                ) -> Any:
    user = crud_user.get_user(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="该邮箱已存在！",
        )
    user = crud_user.create(db, user_in)
    return user
