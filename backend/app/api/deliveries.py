"""Deliveries API router implementation."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas.common import SuccessResponse
from app.schemas.deliveries import DeliveryCreateRequest, DeliveryResponse
from app.services import delivery_service

router = APIRouter(prefix="/api/deliveries", tags=["Deliveries"])


@router.get("/", response_model=SuccessResponse[list[DeliveryResponse]])
def list_deliveries(
    status: str | None = Query(default=None, description="Filter by delivery status"),
    session: Session = Depends(get_session),
) -> SuccessResponse[list[DeliveryResponse]]:
    """List deliveries, optionally filtered by status."""

    try:
        deliveries = delivery_service.list_deliveries(session, status=status)
        return SuccessResponse(data=deliveries)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=SuccessResponse[DeliveryResponse])
def create_delivery(
    request: DeliveryCreateRequest,
    session: Session = Depends(get_session),
) -> SuccessResponse[DeliveryResponse]:
    """Create delivery for completed production."""

    try:
        delivery = delivery_service.create_delivery_for_order(
            session,
            request.sales_order_id,
            request.delivery_date,
        )
        return SuccessResponse(data=delivery)
    except delivery_service.InvalidTransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{delivery_id}/complete", response_model=SuccessResponse[DeliveryResponse])
def mark_delivery_complete(
    delivery_id: int,
    session: Session = Depends(get_session),
) -> SuccessResponse[DeliveryResponse]:
    """Mark delivery as completed and update sales order."""

    try:
        delivery = delivery_service.mark_delivery_done(session, delivery_id)
        return SuccessResponse(data=delivery)
    except delivery_service.EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Delivery not found")
    except delivery_service.InvalidTransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
