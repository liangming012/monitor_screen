from typing import Dict, Union
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.show_model import ShowModel
from schemas.show import ShowCreate, Show


class CRUDShow(CRUDBase):

    def create(self, db: Session, obj_in: ShowCreate) -> ShowModel:
        db_obj = ShowModel(
            screen_id=obj_in.screen_id,
            weight=obj_in.weight,
            project_id=obj_in.project_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ShowModel, obj_in: Union[Show, Dict]) -> ShowModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_show = CRUDShow(ShowModel)

