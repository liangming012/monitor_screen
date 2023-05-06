from typing import Optional

from pydantic import BaseModel


# 基础属性
class NoticeBase(BaseModel):
    name: Optional[str] = None
    webhook_url: Optional[str] = ''
    notice_type: Optional[int] = 0
    at_all: Optional[bool] = False
    remarks: Optional[str] = ''


# 创建通知
class NoticeCreate(NoticeBase):
    pass


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

