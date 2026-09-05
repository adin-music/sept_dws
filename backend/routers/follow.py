from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.social import UserFollow, UserInterest
from schemas.social import FollowRequest, InterestUpdate

router = APIRouter(prefix="/api/follow", tags=["Pracenje"])


@router.post("")
def toggle_follow(data: FollowRequest, db: Session = Depends(get_db)):
    if data.follower_id == data.followed_user_id:
        raise HTTPException(status_code=400, detail="Ne možete pratiti sami sebe")
    existing = db.query(UserFollow).filter_by(
        follower_id=data.follower_id,
        followed_user_id=data.followed_user_id,
    ).first()
    if existing:
        db.delete(existing)
        db.commit()
        return {"following": False}
    db.add(UserFollow(follower_id=data.follower_id, followed_user_id=data.followed_user_id))
    db.commit()
    return {"following": True}


@router.get("/{user_id}")
def list_following(user_id: int, db: Session = Depends(get_db)):
    rows = db.query(UserFollow).filter_by(follower_id=user_id).all()
    return {"following_ids": [r.followed_user_id for r in rows]}


@router.post("/interests")
def set_interests(data: InterestUpdate, db: Session = Depends(get_db)):
    db.query(UserInterest).filter_by(user_id=data.user_id).delete()
    for category in data.categories:
        db.add(UserInterest(user_id=data.user_id, category=category))
    db.commit()
    return {"status": "ok", "categories": data.categories}


@router.get("/interests/{user_id}")
def get_interests(user_id: int, db: Session = Depends(get_db)):
    rows = db.query(UserInterest).filter_by(user_id=user_id).all()
    return {"categories": [r.category for r in rows]}
