from typing import Dict, Optional, Union

from sqlalchemy.orm import Session

import models
from core.permissions import Permissions
from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
from models import User
from schemas.user import UserCreate


class CRUDUser(CRUDBase):

    def get_user(self, db: Session, email: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> models.User:
        db_obj = models.User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            roles=obj_in.roles,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: models.User, obj_in: Union[User, Dict]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, email: str, password: str) -> Optional[models.User]:
        user = self.get_user(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: models.User) -> bool:
        return user.is_active

    def is_superuser(self, user: models.User) -> bool:
        return Permissions.ADMIN.value in user.roles.split(',')


crud_user = CRUDUser(User)

