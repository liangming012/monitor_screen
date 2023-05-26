from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class RecordModel(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    build_id: Mapped[int] = mapped_column(nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False, default=0)
    status: Mapped[int] = mapped_column(nullable=False)  # 0=>成功 1=>失败 2=>超时 999=>失效
    url: Mapped[str] = mapped_column(String(500), default=True)
    check_time: Mapped[int] = mapped_column(nullable=False)
    create_time: Mapped[int] = mapped_column(nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), nullable=False)

    project: Mapped["ProjectModel"] = relationship(back_populates="records")

    def __repr__(self) -> str:
        return f"RecordModel(id={self.id!r}, build_id={self.build_id!r}, duration={self.duration!r}, " \
               f"status={self.status!r}, url={self.url!r}, check_time={self.check_time!r}, " \
               f"create_time={self.create_time!r}, project_id={self.project_id!r}, project={self.project!r})"
