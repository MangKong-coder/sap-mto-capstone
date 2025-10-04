"""
Reporting API endpoints.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.reporting import (
    OrderFlowResponse,
    ProductionStatusSummaryResponse,
    ComponentConsumptionResponse,
    OrderComponentUsageResponse,
    CustomerSummaryResponse,
)
from app.services import (
    get_order_full_flow,
    get_production_status_summary,
    get_component_consumption_summary,
    get_order_component_usage_summary,
    get_customer_order_summary,
    ReportingServiceError,
    ReportNotFoundError,
)


router = APIRouter(prefix="/reporting", tags=["Reporting"])


@router.get("/orders/{order_id}/flow", response_model=OrderFlowResponse)
def get_order_flow(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """Trace order through full MTO flow."""
    try:
        result = get_order_full_flow(db, order_id)
        return result
    except ReportNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ReportingServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/production-status", response_model=ProductionStatusSummaryResponse)
def get_production_summary(
    db: Session = Depends(get_db_session)
):
    """Summarize work order statuses."""
    try:
        result = get_production_status_summary(db)
        return result
    except ReportingServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/component-consumption", response_model=List[ComponentConsumptionResponse])
def get_component_consumption(
    db: Session = Depends(get_db_session)
):
    """Aggregate component usage across all work orders."""
    try:
        results = get_component_consumption_summary(db)
        return results
    except ReportingServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/orders/{order_id}/component-usage", response_model=OrderComponentUsageResponse)
def get_order_component_usage(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """Get component usage summary for an order."""
    try:
        result = get_order_component_usage_summary(db, order_id)
        return result
    except ReportNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ReportingServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/customers/{customer_id}/summary", response_model=CustomerSummaryResponse)
def get_customer_summary(
    customer_id: int,
    db: Session = Depends(get_db_session)
):
    """Get customer order summary."""
    try:
        result = get_customer_order_summary(db, customer_id)
        return result
    except ReportNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ReportingServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/orders/summary")
def get_legacy_order_summary(
    db: Session = Depends(get_db_session)
) -> Dict[str, Any]:
    """Legacy order summary endpoint."""
    # This endpoint provides basic order statistics
    from app.models import Order, OrderStatus
    
    total_orders = db.query(Order).count()
    new_orders = db.query(Order).filter(Order.status == OrderStatus.NEW).count()
    confirmed_orders = db.query(Order).filter(Order.status == OrderStatus.CONFIRMED).count()
    completed_orders = db.query(Order).filter(Order.status == OrderStatus.COMPLETED).count()
    cancelled_orders = db.query(Order).filter(Order.status == OrderStatus.CANCELLED).count()
    
    return {
        "total_orders": total_orders,
        "new": new_orders,
        "confirmed": confirmed_orders,
        "completed": completed_orders,
        "cancelled": cancelled_orders,
    }
