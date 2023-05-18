from typing import Optional, List
from pydantic import BaseModel


# 基础属性
class ShowBase(BaseModel):
    screen_id: Optional[int] = None
    weight: Optional[int] = None
    project_id: Optional[int] = None


# 创建展示项目
class ShowCreate(ShowBase):
    pass


# 修改展示项目
class ShowUpdate(ShowBase):
    pass


# 数据库基础属性
class ShowInDBBase(ShowBase):
    id: Optional[int] = None

    # 关联ORM
    class Config:
        orm_mode = True


# API返回展示项目信息
class Show(ShowInDBBase):
    pass


# API返回展示项目信息
class Shows(BaseModel):
    records: List[Show]
    total: int
