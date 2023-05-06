from typing import Dict, Optional, Union
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.notice_model import NoticeModel
from schemas.notice import Notice


class CRUDNotice(CRUDBase):

    def get_notice(self, db: Session, name: str) -> Optional[NoticeModel]:
        return db.query(NoticeModel).filter(NoticeModel.name == name).first()

    def update(self, db: Session, db_obj: NoticeModel, obj_in: Union[Notice, Dict]) -> NoticeModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


crud_notice = CRUDNotice(NoticeModel)

