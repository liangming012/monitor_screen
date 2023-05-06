from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(50), index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    roles: Mapped[str] = mapped_column(String(500), default=False)

    def __repr__(self) -> str:
        return f"UserModel(id={self.id!r}, full_name={self.full_name!r}, email={self.email!r}), " \
               f"is_active={self.is_active!r}, roles={self.roles!r})"
