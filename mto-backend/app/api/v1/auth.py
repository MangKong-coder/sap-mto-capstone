from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.db.models import User
from app.schemas.auth import UserCreate, UserResponse

router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Note: In a real app, you'd hash the password here
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password,  # Should be hashed!
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
