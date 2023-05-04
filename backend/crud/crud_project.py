from typing import Dict, Optional, Union
from sqlalchemy.orm import Session
import models
import schemas
from crud.base import CRUDBase
from schemas.project import ProjectCreate


class CRUDProject(CRUDBase):

    def get_project(self, db: Session, name: str) -> Optional[models.Project]:
        return db.query(models.Project).filter(models.Project.name == name).first()

    def create(self, db: Session, obj_in: ProjectCreate) -> models.Project:
        db_obj = models.Project(
            name=obj_in.name,
            enable=obj_in.enable,
            duration_limit=obj_in.duration_limit,
            jenkins_url=obj_in.jenkins_url,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: models.Project, obj_in: Union[schemas.Project, Dict]) -> models.Project:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_project = CRUDProject(models.Project)

