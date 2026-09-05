from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from database.db import Base

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    file_path = Column(String, nullable=True)  # Putanja do spremljenog fajla
    is_read = Column(Boolean, default=False)   # Administrator vidi kao nepročitano
    created_at = Column(DateTime, default=datetime.utcnow)