from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class ProjectModel(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    duration_limit: Mapped[int] = mapped_column(index=True, nullable=False, default=0)
    jenkins_url: Mapped[str] = mapped_column(String(500), nullable=False, default='')
    enable: Mapped[bool] = mapped_column(default=True)

    records: Mapped[List["RecordModel"]] = relationship(back_populates="project", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"ProjectModel(id={self.id!r}, name={self.name!r}, duration_limit={self.duration_limit!r}), " \
               f"jenkins_url={self.jenkins_url!r}, enable={self.enable!r})"
