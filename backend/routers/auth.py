import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database.db import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, UserRole, UserResponse, TokenResponse

SECRET_KEY  = "super_tajni_kljuc_za_jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/api/auth",tags=["Auth"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password:str,hashed_password:str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)
def create_access_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

@router.post("/register",response_model=UserResponse)
def register(user_data: UserCreate,db: Session = Depends(get_db)):
    # dont let random people register as admin lol
    if user_data.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="cannot register as admin")
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400,detail="Korisničko ime zauzeto.")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email je već u upotrebi")

    hashrd_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username = user_data.username,
        hashed_password = hashrd_pwd,
        role = user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login",response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Pogrešno korisničko ime ili lozinka.")

    token = create_access_token({"sub": user.username, "role": user.role.value})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username,
        "user_id": user.id,
        "email": user.email
    }
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    return user