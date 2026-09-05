from sqlalchemy import Column, Integer, Text, ForeignKey
from database.db import Base

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    text = Column(Text)

class SavedPost(Base):
    __tablename__ = "saved_posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))