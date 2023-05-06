from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps
from crud.crud_watch_notice import crud_watch_notice
from models.user_model import UserModel
from schemas.msg import Msg
from schemas.watch_notice import WatchNotice, WatchNoticeCreate, WatchNoticeUpdate

router = APIRouter()


@router.get("/", response_model=List[WatchNotice])
def get_watch_notices(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取监控通知列表
    """
    watch_notices = crud_watch_notice.get_multi(db, skip=skip, limit=limit)
    return watch_notices


@router.get("/{watch_notice_id}", response_model=WatchNotice)
def read_watch_notice_by_id(
    watch_notice_id: int,
    current_user: UserModel = Depends(deps.active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    通过id获取监控通知信息
    """
    watch_notice = crud_watch_notice.get(db, unique_id=watch_notice_id)
    return watch_notice


@router.put("/{watch_notice_id}", response_model=WatchNotice)
def update_watch_notice(
    *,
    db: Session = Depends(deps.get_db),
    watch_notice_id: int,
    watch_notice_in: WatchNoticeUpdate,
    current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    修改监控通知信息
    """
    watch_notice = crud_watch_notice.get(db, unique_id=watch_notice_id)
    if not watch_notice:
        raise HTTPException(
            status_code=404,
            detail="找不到该监控通知！",
        )
    watch_notice = crud_watch_notice.update(db, db_obj=watch_notice, obj_in=watch_notice_in)
    return watch_notice


@router.delete("/{watch_notice_id}", response_model=Msg)
def delete_watch_notice_by_id(
    watch_notice_id: int,
    current_user: UserModel = Depends(deps.active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    删除监控通知
    """
    watch_notice = crud_watch_notice.get(db, unique_id=watch_notice_id)
    if not watch_notice:
        raise HTTPException(
            status_code=404,
            detail="找不到该监控通知！",
        )
    crud_watch_notice.remove(db, watch_notice_id)
    return Msg(msg='删除成功！')


@router.post("/", response_model=WatchNotice)
def create_watch_notice(watch_notice_in: WatchNoticeCreate,
                db: Session = Depends(deps.get_db),
                current_user: UserModel = Depends(deps.active_user)
                ) -> Any:
    watch_notice = crud_watch_notice.create(db, watch_notice_in)
    return watch_notice
