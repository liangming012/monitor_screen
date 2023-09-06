from typing import Optional, List

from pydantic import BaseModel


# 基础属性
class ProjectBase(BaseModel):
    name: Optional[str] = None
    enable: Optional[bool] = True
    duration_limit: Optional[int] = None
    jenkins_url: Optional[str] = None


# 创建项目
class ProjectCreate(ProjectBase):
    name: str


# 修改项目
class ProjectUpdate(ProjectBase):
    pass


# 数据库基础属性
class ProjectInDBBase(ProjectBase):
    id: Optional[int] = None

    # 关联ORM
    class Config:
        orm_mode = True


# API返回项目信息
class Project(ProjectInDBBase):
    pass


# API返回项目信息
class Projects(BaseModel):
    records: List[Project]
    total: int
