from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.post import PostResponse
from services.trending import get_trending_posts
from routers.post_helpers import map_post

router = APIRouter(prefix="/api/trending", tags=["Trending"])


@router.get("", response_model=list[PostResponse])
def trending(period: str = "24h", db: Session = Depends(get_db)):
    posts = get_trending_posts(db, period)
    return [map_post(db, p) for p in posts]
