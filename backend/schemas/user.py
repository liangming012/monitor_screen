from typing import Optional, List

from pydantic import BaseModel, EmailStr


# 公共属性
from core.permissions import Permissions


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


# 修改密码
class UserUpdate(UserBase):
    password: Optional[str] = None


# 数据库保存基础属性
class UserInDBBase(UserBase):
    id: Optional[int] = None

    # 关联ORM
    class Config:
        orm_mode = True


# API返回用户信息
class User(UserInDBBase):
    pass

