import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base


class ContentType(str, enum.Enum):
    CLANAK = "clanak"
    KRATKA_OBJAVA = "kratka_objava"
    TUTORIJAL = "tutorijal"
    LINK = "link"
    INFOGRAFIKA = "infografika"


class Category(str, enum.Enum):
    NAUKA = "nauka"
    TEHNOLOGIJA = "tehnologija"
    HISTORIJA = "historija"
    KULTURA = "kultura"
    ZDRAVLJE = "zdravlje"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    file_path = Column(String, nullable=True)
    link_url = Column(String, nullable=True)
    content_type = Column(Enum(ContentType), default=ContentType.CLANAK, nullable=False)
    category = Column(Enum(Category), default=Category.TEHNOLOGIJA, nullable=False)
    views = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    read_time_minutes = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="posts")
