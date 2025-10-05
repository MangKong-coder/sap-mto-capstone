"""
Order API endpoints.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderEnrichedResponse,
    OrderStatusResponse,
)
from app.schemas.planned_order import PlannedOrderResponse
from app.schemas.delivery_schema import DeliveryResponse
from app.schemas.invoice import InvoiceResponse
from app.services import (
    place_order,
    cancel_order,
    get_order_status,
    list_orders_by_customer,
    get_order_by_id_service,
    list_orders_service,
    list_orders_enriched,
    get_order_enriched,
    list_planned_orders_by_order,
    list_deliveries_by_order,
    list_invoices_by_order,
    OrderValidationError,
    OrderNotFoundError,
    OrderCancellationError,
)


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db_session)
):
    """Place a new order."""
    try:
        result = place_order(
            db, 
            order.customer_id, 
            order.items,
            delivery_date=order.delivery_date,
            priority=order.priority or "STANDARD",
            work_center_id=order.work_center_id
        )
        return result
    except OrderValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """Cancel an order."""
    try:
        result = cancel_order(db, order_id)
        return result
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except OrderCancellationError as e:
        raise HTTPException(status_code=409, detail=str(e))





@router.get("/{order_id}/status", response_model=OrderStatusResponse)
def get_order_status_endpoint(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """Get order status with full details."""
    try:
        result = get_order_status(db, order_id)
        return result
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{order_id}/planned-orders", response_model=List[PlannedOrderResponse])
def list_order_planned_orders(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """List planned orders for an order."""
    try:
        results = list_planned_orders_by_order(db, order_id)
        return results
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{order_id}/deliveries", response_model=List[DeliveryResponse])
def list_order_deliveries(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """List deliveries for an order."""
    try:
        results = list_deliveries_by_order(db, order_id)
        return results
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{order_id}/invoices", response_model=List[InvoiceResponse])
def list_order_invoices(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """List invoices for an order."""
    try:
        results = list_invoices_by_order(db, order_id)
        return results
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/customer/{customer_id}", response_model=List[OrderResponse])
def list_orders_by_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db_session)
):
    """List orders by customer."""
    try:
        results = list_orders_by_customer(db, customer_id)
        return results
    except OrderValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/enriched", response_model=List[Dict[str, Any]])
def list_orders_enriched_endpoint(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List orders with full customer and product details."""
    skip = (page - 1) * size
    results = list_orders_enriched(db, skip=skip, limit=size)
    return results


@router.get("/{order_id}/enriched", response_model=Dict[str, Any])
def get_order_enriched_endpoint(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """Get order with full customer and product details."""
    try:
        result = get_order_enriched(db, order_id)
        return result
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[OrderResponse])
def list_orders(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List orders with pagination."""
    skip = (page - 1) * size
    results = list_orders_service(db, skip=skip, limit=size)
    return results

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """Get order by ID."""
    try:
        result = get_order_by_id_service(db, order_id)
        return result
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))