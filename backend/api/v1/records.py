from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps
from crud.crud_record import crud_record
from models.user_model import UserModel
from schemas.msg import Msg
from schemas.record import Record, RecordUpdate, RecordCreate

router = APIRouter()


@router.get("/", response_model=List[Record])
def get_records(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取项目列表
    """
    records = crud_record.get_multi(db, skip=skip, limit=limit)
    return records


@router.get("/{record_id}", response_model=Record)
def read_record_by_id(
        record_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    通过id获取项目信息
    """
    record = crud_record.get(db, unique_id=record_id)
    return record


@router.put("/{record_id}", response_model=Record)
def update_record(
        *,
        db: Session = Depends(deps.get_db),
        record_id: int,
        record_in: RecordUpdate,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    修改项目信息
    """
    record = crud_record.get(db, unique_id=record_id)
    if not record:
        raise HTTPException(
            status_code=404,
            detail="找不到该项目！",
        )
    record = crud_record.update(db, db_obj=record, obj_in=record_in)
    return record


@router.delete("/{record_id}", response_model=Msg)
def delete_record_by_id(
        record_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    删除项目
    """
    record = crud_record.get(db, unique_id=record_id)
    if not record:
        raise HTTPException(
            status_code=404,
            detail="找不到该项目！",
        )
    crud_record.remove(db, record_id)
    return Msg(msg='删除成功！')


@router.post("/", response_model=Record)
def create_record(record_in: RecordCreate,
                  db: Session = Depends(deps.get_db),
                  current_user: UserModel = Depends(deps.active_user)
                  ) -> Any:
    record = crud_record.create(db, record_in)
    return record
