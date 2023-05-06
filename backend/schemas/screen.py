from typing import Optional

from pydantic import BaseModel


# 基础属性
class ScreenBase(BaseModel):
    name: Optional[str] = None
    show_type: Optional[int] = None


# 创建项目
class ScreenCreate(ScreenBase):
    pass


# 修改项目
class ScreenUpdate(ScreenBase):
    pass


# 数据库基础属性
class ScreenInDBBase(ScreenBase):
    id: Optional[int] = None

    # 关联ORM
    class Config:
        orm_mode = True


# API返回项目信息
class Screen(ScreenInDBBase):
    pass

