from database.db import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class UserGroup(Base):
    __tablename__ = "user_group"

    group_id = Column(String, ForeignKey("groups.group_id"), primary_key=True)
    user_line_id = Column(String, ForeignKey("users.line_id"), primary_key=True)

    user = relationship("Users", back_populates="user_groups")
    group = relationship("Groups", back_populates="user_groups")
