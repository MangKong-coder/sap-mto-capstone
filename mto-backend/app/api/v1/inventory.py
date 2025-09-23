from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.db.models import Inventory
from app.schemas.inventory import InventoryResponse

router = APIRouter()


@router.get("/inventory", response_model=List[InventoryResponse])
def get_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()


@router.get("/inventory/{product_id}", response_model=InventoryResponse)
def get_product_inventory(product_id: int, db: Session = Depends(get_db)):
    return db.query(Inventory).filter(Inventory.product_id == product_id).first()
