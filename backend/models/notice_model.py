from sqlalchemy import String, false
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class NoticeModel(Base):
    __tablename__ = "notice"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    notice_type: Mapped[str] = mapped_column(String(500))  # 钉钉、飞书
    webhook_url: Mapped[str] = mapped_column(String(500), default='', nullable=False)
    at_all: Mapped[bool] = mapped_column(default=False, nullable=False)
    watch_type: Mapped[int] = mapped_column(default=1, nullable=False)  # 监控方式： 1 按屏幕  2 按项目
    screen_ids: Mapped[str] = mapped_column(String(500))  # 屏幕列表
    project_ids: Mapped[str] = mapped_column(String(500))  # 项目列表
    faild_count: Mapped[int] = mapped_column(default=1, nullable=False)
    timeout_count: Mapped[int] = mapped_column(default=1, nullable=False)
    remarks: Mapped[str] = mapped_column(String(500), nullable=False)
    enable: Mapped[bool] = mapped_column(default=False,
                                         server_default=false())  # server_default=false() 设置 alembic里的默认值

    def __repr__(self) -> str:
        return f"NoticeModel(id={self.id!r}, name={self.name!r}, webhook_url={self.webhook_url!r}, " \
               f"notice_type={self.notice_type!r}, at_all={self.at_all!r}, remarks={self.remarks!r}, " \
               f"watch_type={self.watch_type!r}, screen_ids={self.screen_ids!r}, project_ids={self.project_ids!r}, " \
               f"faild_count={self.faild_count!r}, timeout_count={self.timeout_count!r}, enable={self.enable!r})"
