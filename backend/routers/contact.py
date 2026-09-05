import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database.db import get_db
from models.contact import ContactMessage
from schemas.contact import ContactMessageResponse

router = APIRouter(prefix="/api/contact", tags=["Contact"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("", response_model=ContactMessageResponse)
async def create_contact_message(
    email: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    saved_file_path = None

    if file:
        # Generisanje unikatnog imena fajla radi izbjegavanja kolizije
        ext = file.filename.split(".")[-1] if "." in file.filename else ""
        filename = f"{uuid.uuid4()}{'.' + ext if ext else ''}"
        saved_file_path = os.path.join(UPLOAD_DIR, filename)

        with open(saved_file_path, "wb") as f:
            content = await file.read()
            f.write(content)

    new_msg = ContactMessage(
        email=email,
        message=message,
        file_path=saved_file_path,
        is_read=False
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    
    return new_msg