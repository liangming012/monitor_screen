from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class NoticeModel(Base):
    __tablename__ = "notice"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    webhook_url: Mapped[str] = mapped_column(String(500), default='', nullable=False)
    notice_type: Mapped[int] = mapped_column(default=0, nullable=False)
    at_all: Mapped[bool] = mapped_column(default=False, nullable=False)
    remarks: Mapped[str] = mapped_column(String(500), nullable=False)

    watch_notices: Mapped[List["WatchNoticeModel"]] = relationship(back_populates="watch_notice",
                                                                   cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"NoticeModel(id={self.id!r}, name={self.name!r}, webhook_url={self.webhook_url!r}, " \
               f"notice_type={self.notice_type!r}, at_all={self.at_all!r}, remarks={self.remarks!r})"



