from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps
from crud.crud_notice import crud_notice
from models.user_model import UserModel
from schemas.msg import Msg
from schemas.notice import NoticeCreate, Notice, NoticeUpdate, Notices

router = APIRouter()


@router.get("/", response_model=Notices)
def get_notices(
        db: Session = Depends(deps.get_db),
        name: str = '',
        current: int = 1,
        size: int = 10,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取报警群组列表
    """
    total = crud_notice.get_notices_count(db, name=name)
    if total:
        notices = crud_notice.get_notices(db, name=name, skip=(current - 1) * size, limit=size)
    else:
        notices = []
    return Notices(records=notices, total=total)


@router.get("/list", response_model=List[Notice])
def notice_list(
        db: Session = Depends(deps.get_db),
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取报警群组列表
    """
    notices = crud_notice.list(db)
    return notices


@router.get("/{notice_id}", response_model=Notice)
def read_notice_by_id(
        notice_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    通过id获取通知信息
    """
    notice = crud_notice.get(db, unique_id=notice_id)
    return notice


@router.put("/{notice_id}", response_model=Notice)
def update_notice(
        *,
        db: Session = Depends(deps.get_db),
        notice_id: int,
        notice_in: NoticeUpdate,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    修改通知信息
    """
    notice = crud_notice.get(db, unique_id=notice_id)
    if not notice:
        raise HTTPException(
            status_code=404,
            detail="找不到该该报警群组！",
        )
    notice = crud_notice.update(db, db_obj=notice, obj_in=notice_in)
    return notice


@router.delete("/{notice_id}", response_model=Msg)
def delete_notice_by_id(
        notice_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    删除通知
    """
    notice = crud_notice.get(db, unique_id=notice_id)
    if not notice:
        raise HTTPException(
            status_code=404,
            detail="找不到该该报警群组！",
        )
    crud_notice.remove(db, notice_id)
    return Msg(msg='删除成功！')


@router.post("/", response_model=Notice)
def create_notice(notice_in: NoticeCreate,
                  db: Session = Depends(deps.get_db),
                  current_user: UserModel = Depends(deps.active_user)
                  ) -> Any:
    notice = crud_notice.get_notice(db, notice_in.name)
    if notice:
        raise HTTPException(
            status_code=400,
            detail="该报警群组已存在！",
        )
    notice = crud_notice.create(db, notice_in)
    return notice
