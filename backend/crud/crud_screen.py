from typing import Dict, Optional, Union
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.screen_model import ScreenModel
from schemas.screen import ScreenCreate, Screen


class CRUDScreen(CRUDBase):

    def get_screen(self, db: Session, name: str) -> Optional[ScreenModel]:
        return db.query(ScreenModel).filter(ScreenModel.name == name).first()

    def create(self, db: Session, obj_in: ScreenCreate) -> ScreenModel:
        db_obj = ScreenModel(
            name=obj_in.name,
            show_type=obj_in.show_type,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ScreenModel, obj_in: Union[Screen, Dict]) -> ScreenModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_screen = CRUDScreen(ScreenModel)

