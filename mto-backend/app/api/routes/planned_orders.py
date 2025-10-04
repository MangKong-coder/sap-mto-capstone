"""
Planned Order API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.planned_order import (
    PlannedOrderCreate,
    PlannedOrderUpdate,
    PlannedOrderResponse,
)
from app.schemas.work_order import WorkOrderResponse
from app.services import (
    generate_planned_order,
    update_planned_order_status,
    convert_to_work_order,
    get_planned_order_by_id_service,
    list_planned_orders_service,
    PlannedOrderValidationError,
    PlannedOrderNotFoundError,
    ConversionError,
)


router = APIRouter(prefix="/planned-orders", tags=["Planned Orders"])


@router.post("", response_model=PlannedOrderResponse, status_code=201)
def create_planned_order(
    planned_order: PlannedOrderCreate,
    db: Session = Depends(get_db_session)
):
    """Generate a planned order from order item."""
    try:
        result = generate_planned_order(db, planned_order.model_dump())
        return result
    except PlannedOrderValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{planned_order_id}", response_model=PlannedOrderResponse)
def update_planned_order(
    planned_order_id: int,
    planned_order: PlannedOrderUpdate,
    db: Session = Depends(get_db_session)
):
    """Update planned order status/details."""
    try:
        result = update_planned_order_status(
            db, planned_order_id, planned_order.model_dump(exclude_unset=True)
        )
        return result
    except PlannedOrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlannedOrderValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{planned_order_id}/convert", response_model=WorkOrderResponse)
def convert_planned_order_to_work_order(
    planned_order_id: int,
    db: Session = Depends(get_db_session)
):
    """Convert planned order to work order."""
    try:
        result = convert_to_work_order(db, planned_order_id)
        return result
    except PlannedOrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConversionError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{planned_order_id}", response_model=PlannedOrderResponse)
def get_planned_order(
    planned_order_id: int,
    db: Session = Depends(get_db_session)
):
    """Get planned order by ID."""
    try:
        result = get_planned_order_by_id_service(db, planned_order_id)
        return result
    except PlannedOrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[PlannedOrderResponse])
def list_planned_orders(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List all planned orders with pagination."""
    skip = (page - 1) * size
    results = list_planned_orders_service(db, skip=skip, limit=size)
    return results
