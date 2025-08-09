from database.db import Base
from sqlalchemy import Column, String

class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    initial = Column(String, unique = True, index=True)
    line_id = Column(String, unique = True)