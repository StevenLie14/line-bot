from database.db import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    line_id = Column(String, unique = True, primary_key=True)
    initial = Column(String, unique = True, index=True)
    user_groups = relationship("UserGroup", back_populates="user")