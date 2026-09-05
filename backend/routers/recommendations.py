from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.post import PostResponse
from services.recommendation import get_recommended_posts
from routers.post_helpers import map_post

router = APIRouter(prefix="/api/recommendations", tags=["AI Preporuke"])


@router.get("/{user_id}", response_model=list[PostResponse])
def recommended_feed(user_id: int, db: Session = Depends(get_db)):
    posts = get_recommended_posts(db, user_id)
    return [map_post(db, p) for p in posts]
