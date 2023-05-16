from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps
from crud.crud_project import crud_project
from crud.crud_record import crud_record
from models.user_model import UserModel
from schemas.msg import Msg
from schemas.record import Record, RecordUpdate, RecordCreate, Records

router = APIRouter()


@router.get("/", response_model=Records)
def get_records(
        *,
        db: Session = Depends(deps.get_db),
        id: str,
        current: int = 1,
        size: int = 10,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取记录列表
    """
    total = crud_record.get_records_count(db, project_id=id)
    if total:
        records = crud_record.get_records(db, project_id=id, skip=(current - 1) * size, limit=size)
    else:
        records = []
    return Records(records=records, total=total)


@router.get("/{record_id}", response_model=Record)
def read_record_by_id(
        record_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    通过id获取记录信息
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
    修改记录信息
    """
    record = crud_record.get(db, unique_id=record_id)
    if not record:
        raise HTTPException(
            status_code=404,
            detail="找不到该记录！",
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
    删除记录
    """
    record = crud_record.get(db, unique_id=record_id)
    if not record:
        raise HTTPException(
            status_code=404,
            detail="找不到该记录！",
        )
    crud_record.remove(db, record_id)
    return Msg(msg='删除成功！')


@router.post("/", response_model=Record)
def create_record(record_in: RecordCreate,
                  db: Session = Depends(deps.get_db),
                  current_user: UserModel = Depends(deps.active_user)
                  ) -> Any:
    project = crud_project.get(db, unique_id=record_in.project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"找不到项目ID为 {record_in.project_id} 的项目！",
        )
    record = crud_record.create(db, record_in)
    return record
