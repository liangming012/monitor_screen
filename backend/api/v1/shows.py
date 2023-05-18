from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps
from crud.crud_show import crud_show
from models.user_model import UserModel
from schemas.msg import Msg
from schemas.show import Show, ShowUpdate, ShowCreate, Shows

router = APIRouter()


@router.get("/", response_model=Shows)
def get_shows(
        db: Session = Depends(deps.get_db),
        project_id: str = '',
        screen_id: str = '',
        current: int = 1,
        size: int = 10,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取展示项目列表
    """
    total = crud_show.get_records_count(db, project_id=project_id, screen_id=screen_id)
    if total:
        shows = crud_show.get_records(db, project_id=project_id, screen_id=screen_id, skip=(current - 1) * size,
                                      limit=size)
    else:
        shows = []
    return Shows(records=shows, total=total)


@router.get("/{show_id}", response_model=Show)
def read_show_by_id(
        show_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    通过id获取展示项目信息
    """
    show = crud_show.get(db, unique_id=show_id)
    return show


@router.put("/{show_id}", response_model=Show)
def update_show(
        *,
        db: Session = Depends(deps.get_db),
        show_id: int,
        show_in: ShowUpdate,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    修改展示项目信息
    """
    show = crud_show.get(db, unique_id=show_id)
    if not show:
        raise HTTPException(
            status_code=404,
            detail="找不到该展示项目！",
        )
    show = crud_show.update(db, db_obj=show, obj_in=show_in)
    return show


@router.delete("/{show_id}", response_model=Msg)
def delete_show_by_id(
        show_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    删除展示项目
    """
    show = crud_show.get(db, unique_id=show_id)
    if not show:
        raise HTTPException(
            status_code=404,
            detail="找不到该展示项目！",
        )
    crud_show.remove(db, show_id)
    return Msg(msg='删除成功！')


@router.post("/", response_model=Show)
def create_show(show_in: ShowCreate,
                db: Session = Depends(deps.get_db),
                current_user: UserModel = Depends(deps.active_user)
                ) -> Any:
    show = crud_show.create(db, show_in)
    return show
