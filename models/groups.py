from database.db import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Groups(Base):
    __tablename__ = "groups"

    group_id = Column(String, primary_key=True, index=True)
    group_name = Column(String, index=True)

    user_groups = relationship("UserGroup", back_populates="group")