from __future__ import annotations
from typing import TYPE_CHECKING, List
from database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from . import UserGroup

class Groups(Base):
    __tablename__ = "groups"

    group_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    group_name: Mapped[str] = mapped_column(String, index=True)

    user_groups: Mapped[List["UserGroup"]] = relationship("UserGroup", back_populates="group")
