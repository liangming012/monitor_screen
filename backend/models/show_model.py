from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class ShowModel(Base):
    __tablename__ = "show"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    screen_id: Mapped[int] = mapped_column(ForeignKey("screen.id"), nullable=False)
    weight: Mapped[int] = mapped_column(nullable=False, default=0)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), nullable=False)

    screen: Mapped["ScreenModel"] = relationship(back_populates="screen_shows")
    show_project: Mapped["ProjectModel"] = relationship(back_populates="project_shows")

    def __repr__(self) -> str:
        return f"ShowModel(id={self.id!r}, screen_id={self.screen_id!r}, weight={self.weight!r}, " \
               f"project_id={self.project_id!r}, screen={self.screen!r}, show_project={self.show_project!r})"
