from typing import Dict, Optional, Union, List, Any
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.screen_model import ScreenModel
from schemas.screen import Screen


class CRUDScreen(CRUDBase):

    def get_screens_count(self, db: Session, name='') -> int:
        return db.query(self.model).filter(ScreenModel.name.like(f'%{name}%')).count()

    def get_screens(self, db: Session, name='', skip: int = 0, limit: int = 100) -> List[Any]:
        if name:
            return db.query(self.model).filter(ScreenModel.name.like(f'%{name}%')).offset(skip).limit(limit).all()
        else:
            return db.query(self.model).offset(skip).limit(limit).all()

    def get_screen(self, db: Session, name: str) -> Optional[ScreenModel]:
        return db.query(ScreenModel).filter(ScreenModel.name == name).first()

    def update(self, db: Session, db_obj: ScreenModel, obj_in: Union[Screen, Dict]) -> ScreenModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_screen = CRUDScreen(ScreenModel)

