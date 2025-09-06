from __future__ import annotations
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING
from database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from . import Groups, Users

class UserGroup(Base):
    __tablename__ = "user_group"

    group_id: Mapped[str] = mapped_column(String, ForeignKey("groups.group_id"), primary_key=True)
    user_line_id: Mapped[str] = mapped_column(String, ForeignKey("users.line_id"), primary_key=True)

    user: Mapped["Users"] = relationship("Users", back_populates="user_groups")
    group: Mapped["Groups"] = relationship("Groups", back_populates="user_groups")
