from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.post import Post
from models.lajkovi import Like, Comment, SavedPost


def get_trending_posts(db: Session, period: str = "24h", limit: int = 10):
    now = datetime.utcnow()
    if period == "7d":
        since = now - timedelta(days=7)
    else:
        since = now - timedelta(hours=24)

    posts = db.query(Post).filter(Post.created_at >= since).all()
    if not posts:
        posts = db.query(Post).order_by(Post.created_at.desc()).limit(limit).all()

    scored = []
    for post in posts:
        likes = db.query(Like).filter_by(post_id=post.id).count()
        comments = db.query(Comment).filter_by(post_id=post.id).count()
        saves = db.query(SavedPost).filter_by(post_id=post.id).count()
        score = likes * 3 + comments * 2 + saves * 2 + post.views + post.shares_count
        scored.append((score, post))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [post for _, post in scored[:limit]]
