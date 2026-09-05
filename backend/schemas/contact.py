from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ContactMessageResponse(BaseModel):
    id: int
    email: EmailStr
    message: str
    file_path: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True