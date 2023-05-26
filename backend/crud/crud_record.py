import time
from typing import Dict, Union, List, Any
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.record_model import RecordModel
from schemas.record import Record, RecordCreate


class CRUDRecord(CRUDBase):

    def get_records_count(self, db: Session, project_id='') -> int:
        if project_id:
            return db.query(self.model).where(RecordModel.project_id == project_id).count()
        else:
            return db.query(self.model).count()

    def get_records(self, db: Session, project_id='', skip: int = 0, limit: int = 100) -> List[Any]:
        if project_id:
            return db.query(self.model).where(RecordModel.project_id == project_id).order_by(
                RecordModel.id.desc()).offset(skip).limit(limit).all()
        else:
            return db.query(self.model).order_by(RecordModel.id.desc()).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: RecordCreate) -> RecordModel:
        db_obj = RecordModel(
            build_id=obj_in.build_id,
            duration=obj_in.duration,
            status=obj_in.status,
            url=obj_in.url,
            check_time=obj_in.check_time,
            create_time=int(time.time()),
            project_id=obj_in.project_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: RecordModel, obj_in: Union[Record, Dict]) -> RecordModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_record = CRUDRecord(RecordModel)
