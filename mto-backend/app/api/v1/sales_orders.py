from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.crud import sales_orders as crud
from app.schemas.sales_order import SalesOrderCreate, SalesOrderUpdate, SalesOrderResponse

router = APIRouter()


@router.post("/", response_model=SalesOrderResponse, status_code=status.HTTP_201_CREATED)
def create_sales_order(
    order: SalesOrderCreate,
    db: Session = Depends(get_db_session)
):
    return crud.create_sales_order(db, order)


@router.get("/", response_model=List[SalesOrderResponse])
def list_sales_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session)
):
    return crud.get_sales_orders(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=SalesOrderResponse)
def get_sales_order(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    db_order = crud.get_sales_order(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sales order with id {order_id} not found"
        )
    return db_order


@router.patch("/{order_id}", response_model=SalesOrderResponse)
def update_sales_order(
    order_id: int,
    order_update: SalesOrderUpdate,
    db: Session = Depends(get_db_session)
):
    db_order = crud.update_sales_order(db, order_id, order_update)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sales order with id {order_id} not found"
        )
    return db_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sales_order(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    success = crud.delete_sales_order(db, order_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sales order with id {order_id} not found"
        )
    return None


