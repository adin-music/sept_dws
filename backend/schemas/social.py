from pydantic import BaseModel
from typing import List, Optional


class InterestUpdate(BaseModel):
    user_id: int
    categories: List[str]


class FollowRequest(BaseModel):
    follower_id: int
    followed_user_id: int


class CollectionCreate(BaseModel):
    user_id: int
    name: str


class CollectionItemAdd(BaseModel):
    user_id: int
    post_id: int


class ShareRequest(BaseModel):
    user_id: Optional[int] = None
