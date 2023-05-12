from typing import Dict, Optional, Union, List, Any
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.project_model import ProjectModel
from schemas.project import Project


class CRUDProject(CRUDBase):

    def get_projects_count(self, db: Session, name='') -> int:
        return db.query(self.model).filter(ProjectModel.name.like(f'%{name}%')).count()

    def get_projects(self, db: Session, name='', skip: int = 0, limit: int = 100) -> List[Any]:
        if name:
            return db.query(self.model).filter(ProjectModel.name.like(f'%{name}%')).offset(skip).limit(limit).all()
        else:
            return db.query(self.model).offset(skip).limit(limit).all()

    def get_project(self, db: Session, name: str) -> Optional[ProjectModel]:
        return db.query(ProjectModel).filter(ProjectModel.name == name).first()

    def update(self, db: Session, db_obj: ProjectModel, obj_in: Union[Project, Dict]) -> ProjectModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_project = CRUDProject(ProjectModel)

