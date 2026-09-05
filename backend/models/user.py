import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database.db import Base

class UserRole(str,enum.Enum):
    ADMIN = "administrator"
    AUTHOR = "autor"
    READER = "citalac"

class User(Base):
    __tablename__ = "users"

    id= Column(Integer,primary_key=True, index=True)
    email = Column(String,unique=True,index=True,nullable=False)
    username= Column(String,unique=True,index=True,nullable=False)
    hashed_password = Column(String,nullable=False)
    role= Column(Enum(UserRole),default=UserRole.READER, nullable=False)
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")