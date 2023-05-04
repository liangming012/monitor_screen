from typing import Optional
from pydantic import BaseModel, EmailStr
from core.permissions import Permissions


# 基础属性
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    roles: str = Permissions.USER.value
    full_name: Optional[str] = None


# 创建用户
class UserCreate(UserBase):
    email: EmailStr
    password: str
    full_name: str


# 修改用户
class UserUpdate(UserBase):
    password: Optional[str] = None


# 数据库基础属性
class UserInDBBase(UserBase):
    id: Optional[int] = None

    # 关联ORM
    class Config:
        orm_mode = True


# API返回用户信息
class User(UserInDBBase):
    pass

