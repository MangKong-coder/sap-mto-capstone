"""Orders API router implementation."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas.common import ErrorResponse, SuccessResponse
from app.schemas.orders import (
    OrderCreateRequest,
    OrderDetailResponse,
    OrderStatusUpdateRequest,
    OrderSummaryResponse,
)
from app.services import order_service

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("/", response_model=SuccessResponse[list[OrderSummaryResponse]])
def list_orders(
    status: str | None = Query(default=None, description="Filter by order status"),
    customer_id: int | None = Query(default=None, description="Filter by customer ID"),
    session: Session = Depends(get_session),
) -> SuccessResponse[list[OrderSummaryResponse]]:
    """Retrieve all sales orders, optionally filtered by status and/or customer ID."""

    try:
        orders = order_service.get_customer_orders(session, status=status, customer_id=customer_id)
        return SuccessResponse(data=orders)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}", response_model=SuccessResponse[OrderDetailResponse])
def get_order(
    order_id: int,
    session: Session = Depends(get_session),
) -> SuccessResponse[OrderDetailResponse]:
    """Retrieve full order details including items, production, delivery, and billing."""

    try:
        order_details = order_service.get_order_details(session, order_id)
        return SuccessResponse(data=order_details)
    except order_service.EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=SuccessResponse[OrderDetailResponse])
def create_order(
    order_data: OrderCreateRequest,
    session: Session = Depends(get_session),
) -> SuccessResponse[OrderDetailResponse]:
    """Create a new sales order with multiple items."""

    try:
        order = order_service.create_order_with_items(
            session,
            order_data.customer_id,
            order_data.items,
        )
        order_details = order_service.get_order_details(session, order.id)
        return SuccessResponse(data=order_details)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{order_id}/status", response_model=SuccessResponse[OrderDetailResponse])
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdateRequest,
    session: Session = Depends(get_session),
) -> SuccessResponse[OrderDetailResponse]:
    """Update order status (e.g., admin override or cancel)."""

    try:
        updated_order = order_service.update_order_status(
            session,
            order_id,
            status_data.status,
        )
        order_details = order_service.get_order_details(session, updated_order.id)
        return SuccessResponse(data=order_details)
    except order_service.EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except order_service.InvalidTransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{order_id}", response_model=SuccessResponse[dict[str, str]])
def delete_order(
    order_id: int,
    session: Session = Depends(get_session),
) -> SuccessResponse[dict[str, str]]:
    """Delete/cancel a sales order."""

    try:
        deleted = order_service.delete_order(session, order_id)
        return SuccessResponse(data={"message": "Order deleted successfully"})
    except order_service.EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
