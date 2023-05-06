from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps
from crud.crud_screen import crud_screen
from models.user_model import UserModel
from schemas.msg import Msg
from schemas.screen import Screen, ScreenCreate, ScreenUpdate

router = APIRouter()


@router.get("/", response_model=List[Screen])
def get_screen(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取屏幕列表
    """
    screen = crud_screen.get_multi(db, skip=skip, limit=limit)
    return screen


@router.get("/{screen_id}", response_model=Screen)
def read_screen_by_id(
        screen_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    通过id获取屏幕信息
    """
    screen = crud_screen.get(db, unique_id=screen_id)
    return screen


@router.put("/{screen_id}", response_model=Screen)
def update_screen(
        *,
        db: Session = Depends(deps.get_db),
        screen_id: int,
        screen_in: ScreenUpdate,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    修改屏幕信息
    """
    screen = crud_screen.get(db, unique_id=screen_id)
    if not screen:
        raise HTTPException(
            status_code=404,
            detail="找不到该屏幕！",
        )
    screen = crud_screen.update(db, db_obj=screen, obj_in=screen_in)
    return screen


@router.delete("/{screen_id}", response_model=Screen)
def delete_screen_by_id(
        screen_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    删除屏幕
    """
    screen = crud_screen.get(db, unique_id=screen_id)
    if not screen:
        raise HTTPException(
            status_code=404,
            detail="找不到该屏幕！",
        )
    crud_screen.remove(db, screen_id)
    return Msg(msg='删除成功！')


@router.post("/", response_model=Screen)
def create_screen(screen_in: ScreenCreate,
                  db: Session = Depends(deps.get_db),
                  current_user: UserModel = Depends(deps.active_user)
                  ) -> Any:
    screen = crud_screen.get_screen(db, screen_in.name)
    if screen:
        raise HTTPException(
            status_code=400,
            detail="该屏幕已存在！",
        )
    screen = crud_screen.create(db, screen_in)
    return screen
