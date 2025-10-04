from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.crud import production_orders as crud
from app.schemas.production_order import ProductionOrderCreate, ProductionOrderUpdate, ProductionOrderResponse

router = APIRouter()


@router.post("/", response_model=ProductionOrderResponse, status_code=status.HTTP_201_CREATED)
def create_production_order(
    order: ProductionOrderCreate,
    db: Session = Depends(get_db_session)
):
    return crud.create_production_order(db, order)


@router.get("/", response_model=List[ProductionOrderResponse])
def list_production_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session)
):
    return crud.get_production_orders(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=ProductionOrderResponse)
def get_production_order(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    db_order = crud.get_production_order(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Production order with id {order_id} not found"
        )
    return db_order


@router.patch("/{order_id}", response_model=ProductionOrderResponse)
def update_production_order(
    order_id: int,
    order_update: ProductionOrderUpdate,
    db: Session = Depends(get_db_session)
):
    db_order = crud.update_production_order(db, order_id, order_update)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Production order with id {order_id} not found"
        )
    return db_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_production_order(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    success = crud.delete_production_order(db, order_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Production order with id {order_id} not found"
        )
    return None


