from typing import Optional, List

from pydantic import BaseModel


# 基础属性
class ScreenBase(BaseModel):
    name: Optional[str] = None
    row: Optional[int] = None
    col: Optional[int] = None
    faild_count: Optional[int] = None
    timeout_count: Optional[int] = None


# 创建屏幕
class ScreenCreate(ScreenBase):
    pass


# 修改屏幕
class ScreenUpdate(ScreenBase):
    pass


# 数据库基础属性
class ScreenInDBBase(ScreenBase):
    id: Optional[int] = None

    # 关联ORM
    class Config:
        orm_mode = True


# API返回屏幕信息
class Screen(ScreenInDBBase):
    pass


# API返回屏幕信息
class Screens(BaseModel):
    records: List[Screen]
    total: int

