from pydantic import BaseModel

class LikeSchema(BaseModel):
    user_id: int

class CommentSchema(BaseModel):
    user_id: int
    text: str

class SaveSchema(BaseModel):
    user_id: int