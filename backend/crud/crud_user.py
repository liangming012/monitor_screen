from typing import Dict, Optional, Union, List, Any
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.user_model import UserModel
from schemas.user import UserCreate, User
from core.permissions import Permissions
from core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase):

    def get_users_count(self, db: Session, name='') -> int:
        return db.query(self.model).filter(UserModel.full_name.like(f'%{name}%')).count()

    def get_users(self, db: Session, name='', skip: int = 0, limit: int = 100) -> List[Any]:
        if name:
            return db.query(self.model).filter(UserModel.full_name.like(f'%{name}%')).offset(skip).limit(limit).all()
        else:
            return db.query(self.model).offset(skip).limit(limit).all()

    def get_user(self, db: Session, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> UserModel:
        db_obj = UserModel(
            is_active=obj_in.is_active,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            roles=obj_in.roles,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: UserModel, obj_in: Union[User, Dict]) -> UserModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data.keys() and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, email: str, password: str) -> Optional[UserModel]:
        user = self.get_user(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: UserModel) -> bool:
        return user.is_active

    def is_superuser(self, user: UserModel) -> bool:
        return Permissions.ADMIN.value in user.roles.split(',')


crud_user = CRUDUser(UserModel)

