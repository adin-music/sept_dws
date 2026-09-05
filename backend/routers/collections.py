from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.social import Collection, CollectionItem
from schemas.social import CollectionCreate, CollectionItemAdd

router = APIRouter(prefix="/api/collections", tags=["Kolekcije"])


@router.get("/user/{user_id}")
def list_collections(user_id: int, db: Session = Depends(get_db)):
    collections = db.query(Collection).filter_by(user_id=user_id).all()
    result = []
    for col in collections:
        items = db.query(CollectionItem).filter_by(collection_id=col.id).all()
        result.append({
            "id": col.id,
            "name": col.name,
            "items_count": len(items),
            "post_ids": [i.post_id for i in items],
        })
    return result


@router.post("")
def create_collection(data: CollectionCreate, db: Session = Depends(get_db)):
    col = Collection(user_id=data.user_id, name=data.name.strip())
    db.add(col)
    db.commit()
    db.refresh(col)
    return {"id": col.id, "name": col.name}


@router.post("/{collection_id}/items")
def add_to_collection(collection_id: int, data: CollectionItemAdd, db: Session = Depends(get_db)):
    col = db.query(Collection).filter(Collection.id == collection_id, Collection.user_id == data.user_id).first()
    if not col:
        raise HTTPException(status_code=404, detail="Kolekcija nije pronađena")
    exists = db.query(CollectionItem).filter_by(collection_id=collection_id, post_id=data.post_id).first()
    if exists:
        return {"status": "already_exists"}
    db.add(CollectionItem(collection_id=collection_id, post_id=data.post_id))
    db.commit()
    return {"status": "ok"}


@router.delete("/{collection_id}/items/{post_id}")
def remove_from_collection(collection_id: int, post_id: int, user_id: int, db: Session = Depends(get_db)):
    col = db.query(Collection).filter(Collection.id == collection_id, Collection.user_id == user_id).first()
    if not col:
        raise HTTPException(status_code=404, detail="Kolekcija nije pronađena")
    item = db.query(CollectionItem).filter_by(collection_id=collection_id, post_id=post_id).first()
    if item:
        db.delete(item)
        db.commit()
    return {"status": "ok"}
