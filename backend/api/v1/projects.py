from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps
from crud.crud_project import crud_project
from models.user_model import UserModel
from schemas.msg import Msg
from schemas.project import Project, ProjectUpdate, ProjectCreate

router = APIRouter()


@router.get("/", response_model=List[Project])
def get_projects(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取项目列表
    """
    projects = crud_project.get_multi(db, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=Project)
def read_project_by_id(
    project_id: int,
    current_user: UserModel = Depends(deps.active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    通过id获取项目信息
    """
    project = crud_project.get(db, unique_id=project_id)
    return project


@router.put("/{project_id}", response_model=Project)
def update_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    project_in: ProjectUpdate,
    current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    修改项目信息
    """
    project = crud_project.get(db, unique_id=project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="找不到该项目！",
        )
    project = crud_project.update(db, db_obj=project, obj_in=project_in)
    return project


@router.delete("/{project_id}", response_model=Project)
def delete_project_by_id(
    project_id: int,
    current_user: UserModel = Depends(deps.active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    删除项目
    """
    project = crud_project.get(db, unique_id=project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="找不到该项目！",
        )
    crud_project.remove(db, project_id)
    return Msg(msg='删除成功！')


@router.post("/", response_model=Project)
def create_project(project_in: ProjectCreate,
                db: Session = Depends(deps.get_db),
                current_user: UserModel = Depends(deps.active_user)
                ) -> Any:
    project = crud_project.get_project(db, project_in.name)
    if project:
        raise HTTPException(
            status_code=400,
            detail="该项目已存在！",
        )
    project = crud_project.create(db, project_in)
    return project
