from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime
from database.db import Base


class UserInterest(Base):
    __tablename__ = "user_interests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category = Column(String, nullable=False)


class UserFollow(Base):
    __tablename__ = "user_follows"
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    followed_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    __table_args__ = (UniqueConstraint("follower_id", "followed_user_id", name="uq_follow"),)


class Collection(Base):
    __tablename__ = "collections"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class CollectionItem(Base):
    __tablename__ = "collection_items"
    id = Column(Integer, primary_key=True)
    collection_id = Column(Integer, ForeignKey("collections.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    __table_args__ = (UniqueConstraint("collection_id", "post_id", name="uq_collection_post"),)


class PostView(Base):
    __tablename__ = "post_views"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    viewed_at = Column(DateTime, default=datetime.utcnow)
