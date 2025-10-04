"""
Work Order API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.work_order import (
    WorkOrderResponse,
    WorkOrderConfirmRequest,
    WorkOrderConsumeRequest,
)
from app.schemas.component_usage import ComponentUsageResponse
from app.services import (
    start_work_order,
    confirm_work_order,
    consume_components,
    close_work_order,
    get_work_order_by_id_service,
    list_work_orders_service,
    get_work_order_component_usage,
    WorkOrderValidationError,
    WorkOrderNotFoundError,
    WorkOrderStateError,
)


router = APIRouter(prefix="/work-orders", tags=["Work Orders"])


@router.put("/{work_order_id}/start", response_model=WorkOrderResponse)
def start_work_order_endpoint(
    work_order_id: int,
    db: Session = Depends(get_db_session)
):
    """Start a work order."""
    try:
        result = start_work_order(db, work_order_id)
        return result
    except WorkOrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except WorkOrderStateError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{work_order_id}/confirm", response_model=WorkOrderResponse)
def confirm_work_order_endpoint(
    work_order_id: int,
    request: WorkOrderConfirmRequest,
    db: Session = Depends(get_db_session)
):
    """Confirm work order completion."""
    try:
        result = confirm_work_order(db, work_order_id, request.produced_qty)
        return result
    except WorkOrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except WorkOrderValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except WorkOrderStateError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{work_order_id}/consume", response_model=List[ComponentUsageResponse])
def consume_components_endpoint(
    work_order_id: int,
    request: WorkOrderConsumeRequest,
    db: Session = Depends(get_db_session)
):
    """Record component consumption for work order."""
    try:
        results = consume_components(db, work_order_id, request.components)
        return results
    except WorkOrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except WorkOrderValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{work_order_id}/close", response_model=WorkOrderResponse)
def close_work_order_endpoint(
    work_order_id: int,
    db: Session = Depends(get_db_session)
):
    """Close a work order."""
    try:
        result = close_work_order(db, work_order_id)
        return result
    except WorkOrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except WorkOrderStateError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{work_order_id}", response_model=WorkOrderResponse)
def get_work_order(
    work_order_id: int,
    db: Session = Depends(get_db_session)
):
    """Get work order by ID."""
    try:
        result = get_work_order_by_id_service(db, work_order_id)
        return result
    except WorkOrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{work_order_id}/usage", response_model=List[ComponentUsageResponse])
def get_work_order_usage(
    work_order_id: int,
    db: Session = Depends(get_db_session)
):
    """Get component usage for work order."""
    try:
        results = get_work_order_component_usage(db, work_order_id)
        return results
    except WorkOrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[WorkOrderResponse])
def list_work_orders(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List work orders with pagination."""
    skip = (page - 1) * size
    results = list_work_orders_service(db, skip=skip, limit=size)
    return results
