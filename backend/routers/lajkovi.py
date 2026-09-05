from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.lajkovi import Like, Comment, SavedPost
from models.post import Post
from models.user import User
from models.social import PostView, Collection, CollectionItem
from schemas.lajkovi import LikeSchema, CommentSchema, SaveSchema
from schemas.post import PostResponse
from routers.post_helpers import map_post

router = APIRouter(prefix="/api", tags=["Interakcije"])


@router.post("/posts/{post_id}/like")
def toggle_like(post_id: int, data: LikeSchema, db: Session = Depends(get_db)):
    like = db.query(Like).filter_by(post_id=post_id, user_id=data.user_id).first()
    if like:
        db.delete(like)
    else:
        db.add(Like(post_id=post_id, user_id=data.user_id))
    db.commit()
    return {"status": "ok"}


@router.post("/posts/{post_id}/comment")
def add_comment(post_id: int, data: CommentSchema, db: Session = Depends(get_db)):
    db.add(Comment(post_id=post_id, user_id=data.user_id, text=data.text))
    db.commit()
    return {"status": "ok"}


@router.get("/posts/{post_id}/comments")
def get_comments(post_id: int, db: Session = Depends(get_db)):
    # throws comments from database for one post
    comments = db.query(Comment).filter_by(post_id=post_id).all()
    result = []
    for c in comments:
        user = db.query(User).filter(User.id == c.user_id).first()
        result.append({
            "id": c.id,
            "user_id": c.user_id,
            "text": c.text,
            "username": user.username if user else "unknown",
        })
    return result


@router.post("/posts/{post_id}/save")
def toggle_save(post_id: int, data: SaveSchema, db: Session = Depends(get_db)):
    saved = db.query(SavedPost).filter_by(post_id=post_id, user_id=data.user_id).first()
    col = db.query(Collection).filter_by(user_id=data.user_id, name="Moje kolekcije").first()

    if saved:
        db.delete(saved)
        if col:
            item = db.query(CollectionItem).filter_by(collection_id=col.id, post_id=post_id).first()
            if item:
                db.delete(item)
    else:
        db.add(SavedPost(post_id=post_id, user_id=data.user_id))
        if not col:
            col = Collection(user_id=data.user_id, name="Moje kolekcije")
            db.add(col)
            db.flush()
        exists = db.query(CollectionItem).filter_by(collection_id=col.id, post_id=post_id).first()
        if not exists:
            db.add(CollectionItem(collection_id=col.id, post_id=post_id))
    db.commit()
    return {"status": "ok"}


@router.post("/posts/{post_id}/view")
def record_view(post_id: int, user_id: int = None, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Objava nije pronađena")
    post.views = (post.views or 0) + 1
    db.add(PostView(user_id=user_id, post_id=post_id))
    db.commit()
    return {"views": post.views}


@router.get("/posts/saved/{user_id}", response_model=list[PostResponse])
def get_saved_posts(user_id: int, db: Session = Depends(get_db)):
    saved_records = db.query(SavedPost).filter_by(user_id=user_id).all()
    saved_post_ids = [s.post_id for s in saved_records]
    if not saved_post_ids:
        return []
    posts = db.query(Post).filter(Post.id.in_(saved_post_ids)).all()
    return [map_post(db, p) for p in posts]
