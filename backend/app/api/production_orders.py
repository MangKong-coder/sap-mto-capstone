"""Production orders API router implementation."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas.common import SuccessResponse
from app.schemas.production_orders import (
    ProductionOrderResponse,
    ProductionOrderStartRequest,
)
from app.services import production_service

router = APIRouter(prefix="/api/production-orders", tags=["Production Orders"], redirect_slashes=False)


@router.get("/", response_model=SuccessResponse[list[ProductionOrderResponse]])
def list_production_orders(
    status: str | None = Query(default=None, description="Filter by production status"),
    session: Session = Depends(get_session),
) -> SuccessResponse[list[ProductionOrderResponse]]:
    """List all production orders, optionally filtered by status."""

    try:
        production_orders = production_service.list_production_orders(session, status=status)
        return SuccessResponse(data=production_orders)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=SuccessResponse[ProductionOrderResponse])
def start_production(
    request: ProductionOrderStartRequest,
    session: Session = Depends(get_session),
) -> SuccessResponse[ProductionOrderResponse]:
    """Start production for a given sales order."""

    try:
        production_order = production_service.start_production_for_order(
            session,
            request.sales_order_id,
        )
        return SuccessResponse(data=production_order)
    except production_service.InvalidTransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{production_id}/start", response_model=SuccessResponse[ProductionOrderResponse])
def mark_production_in_progress(
    production_id: int,
    session: Session = Depends(get_session),
) -> SuccessResponse[ProductionOrderResponse]:
    """Mark a production order as 'In Progress'."""

    try:
        production_order = production_service.mark_production_in_progress(
            session,
            production_id,
        )
        return SuccessResponse(data=production_order)
    except production_service.EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Production order not found")
    except production_service.InvalidTransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{production_id}/complete", response_model=SuccessResponse[ProductionOrderResponse])
def mark_production_complete(
    production_id: int,
    session: Session = Depends(get_session),
) -> SuccessResponse[ProductionOrderResponse]:
    """Mark production complete and update related sales order."""

    try:
        production_order = production_service.mark_production_complete(
            session,
            production_id,
        )
        return SuccessResponse(data=production_order)
    except production_service.EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Production order not found")
    except production_service.InvalidTransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
