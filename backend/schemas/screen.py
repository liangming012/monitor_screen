from typing import Optional

from pydantic import BaseModel


# 基础属性
class ScreenBase(BaseModel):
    name: Optional[str] = None
    show_type: Optional[int] = None


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

