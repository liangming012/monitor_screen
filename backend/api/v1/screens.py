import time
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api import deps
from crud.crud_project import crud_project
from crud.crud_record import crud_record
from crud.crud_screen import crud_screen
from crud.crud_show import crud_show
from models.user_model import UserModel
from schemas.msg import Msg
from schemas.screen import Screen, ScreenCreate, ScreenUpdate, Screens

router = APIRouter()


@router.get("/", response_model=Screens)
def get_screens(
        db: Session = Depends(deps.get_db),
        name: str = '',
        current: int = 1,
        size: int = 10,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取屏幕列表
    """
    total = crud_screen.get_screens_count(db, name=name)
    if total:
        screens = crud_screen.get_screens(db, name=name, skip=(current - 1) * size, limit=size)
    else:
        screens = []
    return Screens(records=screens, total=total)


@router.get("/list", response_model=List[Screen])
def project_list(
        db: Session = Depends(deps.get_db),
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    获取屏幕列表
    """
    projects = crud_screen.list(db)
    return projects


@router.get("/{screen_id}", response_model=Screen)
def read_screen_by_id(
        screen_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    通过id获取屏幕信息
    """
    screen = crud_screen.get(db, unique_id=screen_id)
    return screen


@router.get("/{screen_id}/show")
def read_screen_by_id(
        screen_id: int,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    通过id获取屏幕信息
    """
    screen = crud_screen.get(db, unique_id=screen_id)
    if not screen:
        raise HTTPException(
            status_code=404,
            detail="找不到该屏幕！",
        )
    shows = crud_show.get_screen_data(db, screen_id)
    total = screen.row * screen.col
    data = []
    for i in range(min(total, len(shows))):
        # status值：0=>成功 1=>失败 2=>超时 999=>失效
        project = {"name": crud_project.get(db, unique_id=shows[i].project_id).name, "status": 999}
        records = crud_record.get_records(db, project_id=shows[i].project_id,
                                          limit=max(screen.faild_count, screen.timeout_count))
        if len(records) > 0:
            project['check_time'] = records[0].check_time
            project['status'] = records[0].status
            if project['status'] == 1 and screen.faild_count > 1:
                for m in range(min(screen.faild_count, len(records))):
                    if records[m].status == 0:
                        if records[m].duration <= records[m].project.duration_limit:
                            project['status'] = 0
                            break
                        else:
                            project['status'] = 2
            elif project['status'] == 2 and screen.timeout_count > 1:
                for m in range(min(screen.timeout_count, len(records))):
                    if records[m].status == 0:
                        if records[m].duration <= records[m].project.duration_limit:
                            project['status'] = 0
                            break
                        else:
                            project['status'] = 2
        else:
            project['check_time'] = int(time.time())
        data.append(project)
    return {"screen": jsonable_encoder(screen), "data": data}


@router.put("/{screen_id}", response_model=Screen)
def update_screen(
        *,
        db: Session = Depends(deps.get_db),
        screen_id: int,
        screen_in: ScreenUpdate,
        current_user: UserModel = Depends(deps.active_user),
) -> Any:
    """
    修改屏幕信息
    """
    screen = crud_screen.get(db, unique_id=screen_id)
    if not screen:
        raise HTTPException(
            status_code=404,
            detail="找不到该屏幕！",
        )
    screen = crud_screen.update(db, db_obj=screen, obj_in=screen_in)
    return screen


@router.delete("/{screen_id}", response_model=Msg)
def delete_screen_by_id(
        screen_id: int,
        current_user: UserModel = Depends(deps.active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    删除屏幕
    """
    screen = crud_screen.get(db, unique_id=screen_id)
    if not screen:
        raise HTTPException(
            status_code=404,
            detail="找不到该屏幕！",
        )
    crud_screen.remove(db, screen_id)
    return Msg(msg='删除成功！')


@router.post("/", response_model=Screen)
def create_screen(screen_in: ScreenCreate,
                  db: Session = Depends(deps.get_db),
                  current_user: UserModel = Depends(deps.active_user)
                  ) -> Any:
    screen = crud_screen.get_screen(db, screen_in.name)
    if screen:
        raise HTTPException(
            status_code=400,
            detail="该屏幕已存在！",
        )
    screen = crud_screen.create(db, screen_in)
    return screen
