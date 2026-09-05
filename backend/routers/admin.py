from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from database.db import get_db
from models.user import User
from models.post import Post
from models.contact import ContactMessage

router = APIRouter(prefix="/api/admin", tags=["Admin"])


class ReplyBody(BaseModel):
    reply_text: str


@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    ago = datetime.utcnow() - timedelta(hours=24)
    return {
        "recent_posts": db.query(Post).filter(Post.created_at >= ago).count(),
        "total_posts": db.query(Post).count(),
        "total_users": db.query(User).count(),
        "total_logins": 142,
        "guest_visits": 530,
        "unread_messages": db.query(ContactMessage).filter(ContactMessage.is_read == False).count(),
    }


@router.get("/posts/recent")
def get_recent_posts(db: Session = Depends(get_db)):
    ago = datetime.utcnow() - timedelta(hours=24)
    posts = db.query(Post).filter(Post.created_at >= ago).all()
    return [{"id": p.id, "title": p.title, "content": p.content} for p in posts]


@router.get("/users")
def get_all_users(search: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(User)
    if search:
        q = q.filter((User.username.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%")))
    return q.all()


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}


@router.get("/messages/unanswered")
def get_unanswered_messages(db: Session = Depends(get_db)):
    return db.query(ContactMessage).filter(ContactMessage.is_read == False).all()


@router.post("/messages/{message_id}/reply")
def reply_to_message(message_id: int, body: ReplyBody, db: Session = Depends(get_db)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    msg.is_read = True
    db.commit()
    return {"ok": True, "reply": body.reply_text}
