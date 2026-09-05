from pydantic import BaseModel, EmailStr
from models.user import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRole = UserRole.READER
class UserLogin(BaseModel):
    username:str
    password: str
class UserResponse(BaseModel):
    id:int
    email: EmailStr
    username: str
    role: UserRole

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: UserRole
    username: str
    user_id: int
    email: str