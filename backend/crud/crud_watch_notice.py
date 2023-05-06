from typing import Dict, Union
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.watch_notice_model import WatchNoticeModel
from schemas.watch_notice import WatchNotice


class CRUDWatchNotice(CRUDBase):

    def update(self, db: Session, db_obj: WatchNoticeModel, obj_in: Union[WatchNotice, Dict]) -> WatchNoticeModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_watch_notice = CRUDWatchNotice(WatchNoticeModel)

