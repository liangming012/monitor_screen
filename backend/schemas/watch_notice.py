from typing import Optional

from pydantic import BaseModel


# 基础属性
class WatchNoticeBase(BaseModel):
    project_id: Optional[int] = None
    notice_id: Optional[int] = None


# 创建通知
class WatchNoticeCreate(WatchNoticeBase):
    pass


# 修改通知
class WatchNoticeUpdate(WatchNoticeBase):
    pass


# 数据库基础属性
class WatchNoticeInDBBase(WatchNoticeBase):
    id: Optional[int] = None

    # 关联ORM
    class Config:
        orm_mode = True


# API返回通知信息
class WatchNotice(WatchNoticeInDBBase):
    pass

