from typing import Optional

from pydantic import BaseModel


# 基础属性
class RecordBase(BaseModel):
    build_id: Optional[int] = None
    duration: Optional[int] = None
    status: Optional[int] = None
    url: Optional[str] = None
    check_time: Optional[int] = None
    project_id: Optional[int] = None


# 创建记录
class RecordCreate(RecordBase):
    build_id: int
    duration: int
    status: int
    url: str
    check_time: int
    project_id: int


# 修改记录
class RecordUpdate(RecordBase):
    pass


# 数据库基础属性
class RecordInDBBase(RecordBase):
    id: Optional[int] = None

    # 关联ORM
    class Config:
        orm_mode = True


# API返回项目信息
class Record(RecordInDBBase):
    create_time: Optional[int] = None

