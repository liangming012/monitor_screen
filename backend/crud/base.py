from typing import Any, Dict, List, Optional, Type, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.base import Base


class CRUDBase:
    def __init__(self, model: Base):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def list(self, db: Session):
        return db.query(self.model).all()

    def get(self, db: Session, unique_id: Any) -> Any:
        return db.query(self.model).filter(self.model.id == unique_id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Any]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: BaseModel) -> Any:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Base,
        obj_in: Union[BaseModel, Dict[str, Any]]
    ) -> Any:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Any:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
