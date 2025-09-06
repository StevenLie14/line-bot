from __future__ import annotations
from typing import TYPE_CHECKING, List
from database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from . import UserGroup
    
class Users(Base):
    __tablename__ = "users"

    line_id: Mapped[str] = mapped_column(String, unique=True, primary_key=True)
    initial: Mapped[str] = mapped_column(String, unique=True, index=True)

    user_groups: Mapped[List["UserGroup"]] = relationship("UserGroup", back_populates="user")
