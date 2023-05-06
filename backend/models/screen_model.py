from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class ScreenModel(Base):
    __tablename__ = "screen"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    show_type: Mapped[int] = mapped_column(default=0, nullable=False)

    def __repr__(self) -> str:
        return f"Screen(id={self.id!r}, name={self.name!r}, show_type={self.show_type!r})"
