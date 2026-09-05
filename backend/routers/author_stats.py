from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from models.post import Post
from models.lajkovi import Like, Comment, SavedPost

router = APIRouter(prefix="/api/author", tags=["Autor statistika"])


@router.get("/stats/{author_id}")
def author_stats(author_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.author_id == author_id).all()
    post_ids = [p.id for p in posts]

    total_views = sum(p.views or 0 for p in posts)
    total_shares = sum(p.shares_count or 0 for p in posts)
    total_read_time = sum(p.read_time_minutes or 1 for p in posts)

    likes = db.query(Like).filter(Like.post_id.in_(post_ids)).count() if post_ids else 0
    comments = db.query(Comment).filter(Comment.post_id.in_(post_ids)).count() if post_ids else 0
    saves = db.query(SavedPost).filter(SavedPost.post_id.in_(post_ids)).count() if post_ids else 0

    return {
        "posts_count": len(posts),
        "total_views": total_views,
        "total_shares": total_shares,
        "total_read_time_minutes": total_read_time,
        "total_likes": likes,
        "total_comments": comments,
        "total_saves": saves,
    }
