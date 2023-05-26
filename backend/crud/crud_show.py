from typing import Dict, Union, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from crud.base import CRUDBase
from models.show_model import ShowModel
from schemas.show import Show


class CRUDShow(CRUDBase):

    def get_shows_count(self, db: Session, project_id='', screen_id='') -> int:
        if project_id and screen_id:
            return db.query(self.model).filter(
                and_(ShowModel.project_id == project_id, ShowModel.screen_id == screen_id)).count()
        elif project_id:
            return db.query(self.model).where(ShowModel.project_id == project_id).count()
        elif screen_id:
            return db.query(self.model).where(ShowModel.screen_id == screen_id).count()
        else:
            return db.query(self.model).count()

    def get_shows(self, db: Session, project_id='', screen_id='', skip: int = 0, limit: int = 100) -> List[Any]:
        if project_id and screen_id:
            return db.query(self.model).filter(
                and_(ShowModel.project_id == project_id, ShowModel.screen_id == screen_id)).offset(skip).limit(
                limit).all()
        elif project_id:
            return db.query(self.model).where(ShowModel.project_id == project_id).offset(skip).limit(limit).all()
        elif screen_id:
            return db.query(self.model).where(ShowModel.screen_id == screen_id).offset(skip).limit(limit).all()
        else:
            return db.query(self.model).offset(skip).limit(limit).all()

    def get_screen_data(self, db: Session, screen_id):
        return db.query(self.model).where(ShowModel.screen_id == screen_id).order_by(ShowModel.weight.desc()).all()

    def update(self, db: Session, db_obj: ShowModel, obj_in: Union[Show, Dict]) -> ShowModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_show = CRUDShow(ShowModel)
