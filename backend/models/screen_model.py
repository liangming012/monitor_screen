from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class ScreenModel(Base):
    __tablename__ = "screen"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    row: Mapped[int] = mapped_column(default=1, nullable=False)
    col: Mapped[int] = mapped_column(default=1, nullable=False)

    shows: Mapped[List["ShowModel"]] = relationship(back_populates="screen", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"ScreenModel(id={self.id!r}, name={self.name!r}, row={self.row!r}, col={self.col!r})"
