from typing import Optional, List

from pydantic import BaseModel


# 基础属性
class NoticeBase(BaseModel):
    name: Optional[str] = None
    notice_type: Optional[str] = ''
    webhook_url: Optional[str] = ''
    at_all: Optional[bool] = False
    watch_type: Optional[int] = 1
    screen_ids: Optional[str] = 1
    project_ids: Optional[str] = 1
    faild_count: Optional[int] = 1
    timeout_count: Optional[int] = 1
    remarks: Optional[str] = ''
    enable: Optional[bool] = False


# 创建通知
class NoticeCreate(NoticeBase):
    name: str


# 修改通知
class NoticeUpdate(NoticeBase):
    pass


# 数据库基础属性
class NoticeInDBBase(NoticeBase):
    id: Optional[int] = None

    # 关联ORM
    class Config:
        orm_mode = True


# API返回通知信息
class Notice(NoticeInDBBase):
    pass


# API返回通知信息
class Notices(BaseModel):
    records: List[Notice]
    total: int



