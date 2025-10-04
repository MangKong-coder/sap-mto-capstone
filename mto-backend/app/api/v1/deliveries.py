from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.crud import deliveries as crud
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate, DeliveryResponse

router = APIRouter()


@router.post("/", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
def create_delivery(
    delivery: DeliveryCreate,
    db: Session = Depends(get_db_session)
):
    return crud.create_delivery(db, delivery)


@router.get("/", response_model=List[DeliveryResponse])
def list_deliveries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session)
):
    return crud.get_deliveries(db, skip=skip, limit=limit)


@router.get("/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(
    delivery_id: int,
    db: Session = Depends(get_db_session)
):
    db_delivery = crud.get_delivery(db, delivery_id)
    if not db_delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Delivery with id {delivery_id} not found"
        )
    return db_delivery


@router.patch("/{delivery_id}", response_model=DeliveryResponse)
def update_delivery(
    delivery_id: int,
    delivery_update: DeliveryUpdate,
    db: Session = Depends(get_db_session)
):
    db_delivery = crud.update_delivery(db, delivery_id, delivery_update)
    if not db_delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Delivery with id {delivery_id} not found"
        )
    return db_delivery


@router.delete("/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delivery(
    delivery_id: int,
    db: Session = Depends(get_db_session)
):
    success = crud.delete_delivery(db, delivery_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Delivery with id {delivery_id} not found"
        )
    return None


