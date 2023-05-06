from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class WatchNoticeModel(Base):
    __tablename__ = "watch_notice"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), nullable=False)
    notice_id: Mapped[int] = mapped_column(ForeignKey("notice.id"), nullable=False)

    watch_project: Mapped["ProjectModel"] = relationship(back_populates="watch_notices")
    watch_notice: Mapped["NoticeModel"] = relationship(back_populates="watch_notices")

    def __repr__(self) -> str:
        return f"RecordModel(id={self.id!r}, name={self.name!r}, duration_limit={self.duration_limit!r}), " \
               f"jenkins_url={self.jenkins_url!r}, enable={self.enable!r})"
