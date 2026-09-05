import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.post import Post, ContentType, Category
from models.user import User
from schemas.post import PostResponse
from routers.post_helpers import map_post

router = APIRouter(prefix="/api/posts", tags=["Posts"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("", response_model=PostResponse)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    author_id: int = Form(...),
    content_type: str = Form("clanak"),
    category: str = Form("tehnologija"),
    link_url: Optional[str] = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    saved_path = None
    if file and file.filename:
        ext = file.filename.split(".")[-1] if "." in file.filename else ""
        filename = f"{uuid.uuid4()}{'.' + ext if ext else ''}"
        saved_path = os.path.join(UPLOAD_DIR, filename)
        with open(saved_path, "wb") as f:
            f.write(await file.read())

    read_time = max(1, len(content.split()) // 200)

    new_post = Post(
        title=title,
        content=content,
        author_id=author_id,
        file_path=saved_path,
        link_url=link_url,
        content_type=ContentType(content_type),
        category=Category(category),
        read_time_minutes=read_time,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return map_post(db, new_post)


@router.get("", response_model=List[PostResponse])
def get_all_posts(
    category: Optional[str] = None,
    content_type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Post)
    if category:
        query = query.filter(Post.category == Category(category))
    if content_type:
        query = query.filter(Post.content_type == ContentType(content_type))
    if search:
        like = f"%{search}%"
        query = query.filter((Post.title.ilike(like)) | (Post.content.ilike(like)))
    posts = query.order_by(Post.created_at.desc()).all()
    return [map_post(db, p) for p in posts]


@router.get("/user/{username}", response_model=List[PostResponse])
def get_posts_by_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return []
    posts = db.query(Post).filter(Post.author_id == user.id).order_by(Post.created_at.desc()).all()
    return [map_post(db, p) for p in posts]


@router.get("/author/{author_id}", response_model=List[PostResponse])
def get_posts_by_author_id(author_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.author_id == author_id).order_by(Post.created_at.desc()).all()
    return [map_post(db, p) for p in posts]


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Objava nije pronađena")
    post.views = (post.views or 0) + 1
    db.commit()
    db.refresh(post)
    return map_post(db, post)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Objava nije pronađena")
    if post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Nemate dozvolu za brisanje ove objave")
    if post.file_path and os.path.exists(post.file_path):
        try:
            os.remove(post.file_path)
        except Exception:
            pass
    db.delete(post)
    db.commit()
    return None
