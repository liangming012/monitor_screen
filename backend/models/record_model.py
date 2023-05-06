from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class RecordModel(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    build_id: Mapped[int] = mapped_column(nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False, default=0)
    status: Mapped[int] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(String(500), default=True)
    check_time: Mapped[int] = mapped_column(nullable=False)
    create_time: Mapped[int] = mapped_column(nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), nullable=False)

    project: Mapped["ProjectModel"] = relationship(back_populates="records")

    def __repr__(self) -> str:
        return f"RecordModel(id={self.id!r}, name={self.name!r}, duration_limit={self.duration_limit!r}), " \
               f"jenkins_url={self.jenkins_url!r}, enable={self.enable!r})"
