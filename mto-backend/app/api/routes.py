from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models

router = APIRouter()

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()
