from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.post import Post
from models.lajkovi import Like, Comment, SavedPost
from schemas.post import PostResponse


def map_post(db: Session, post: Post) -> PostResponse:
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        file_path=post.file_path,
        link_url=getattr(post, "link_url", None),
        content_type=post.content_type.value if hasattr(post.content_type, "value") else str(post.content_type),
        category=post.category.value if hasattr(post.category, "value") else str(post.category),
        views=getattr(post, "views", 0) or 0,
        shares_count=getattr(post, "shares_count", 0) or 0,
        read_time_minutes=getattr(post, "read_time_minutes", 1) or 1,
        created_at=post.created_at,
        author_id=post.author_id,
        author_username=post.author.username if post.author else "Nepoznat",
        likes_count=db.query(Like).filter_by(post_id=post.id).count(),
        comments_count=db.query(Comment).filter_by(post_id=post.id).count(),
        saves_count=db.query(SavedPost).filter_by(post_id=post.id).count(),
    )


router = APIRouter(prefix="/api/posts", tags=["Posts"])
