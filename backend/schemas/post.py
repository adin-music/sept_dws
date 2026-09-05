from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    file_path: Optional[str] = None
    link_url: Optional[str] = None
    content_type: str = "clanak"
    category: str = "tehnologija"
    views: int = 0
    shares_count: int = 0
    read_time_minutes: int = 1
    created_at: datetime
    author_id: int
    author_username: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0
    saves_count: int = 0

    class Config:
        from_attributes = True
