"""
Delivery API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.delivery_schema import (
    DeliveryCreate,
    DeliveryStatusUpdate,
    DeliveryResponse,
)
from app.services import (
    schedule_delivery,
    update_delivery_status,
    get_customer_deliveries,
    get_delivery_by_id_service,
    list_deliveries_service,
    list_deliveries_by_order,
    DeliveryValidationError,
    DeliveryNotFoundError,
)


router = APIRouter(prefix="/deliveries", tags=["Deliveries"])


@router.post("", response_model=DeliveryResponse, status_code=201)
def create_delivery(
    delivery: DeliveryCreate,
    db: Session = Depends(get_db_session)
):
    """Schedule a new delivery."""
    try:
        result = schedule_delivery(db, delivery.model_dump())
        return result
    except DeliveryValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{delivery_id}/status", response_model=DeliveryResponse)
def update_delivery_status_endpoint(
    delivery_id: int,
    status_update: DeliveryStatusUpdate,
    db: Session = Depends(get_db_session)
):
    """Update delivery status."""
    try:
        result = update_delivery_status(
            db, delivery_id, status_update.model_dump(exclude_unset=True)
        )
        return result
    except DeliveryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DeliveryValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(
    delivery_id: int,
    db: Session = Depends(get_db_session)
):
    """Get delivery by ID."""
    try:
        result = get_delivery_by_id_service(db, delivery_id)
        return result
    except DeliveryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/customer/{customer_id}", response_model=List[DeliveryResponse])
def list_customer_deliveries(
    customer_id: int,
    db: Session = Depends(get_db_session)
):
    """List deliveries for a customer."""
    try:
        results = get_customer_deliveries(db, customer_id)
        return results
    except DeliveryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/order/{order_id}", response_model=List[DeliveryResponse])
def list_order_deliveries_endpoint(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """List deliveries for an order."""
    try:
        results = list_deliveries_by_order(db, order_id)
        return results
    except DeliveryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[DeliveryResponse])
def list_deliveries(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List deliveries with pagination."""
    skip = (page - 1) * size
    results = list_deliveries_service(db, skip=skip, limit=size)
    return results
