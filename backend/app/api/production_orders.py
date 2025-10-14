"""Production orders API router implementation."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models import Product
from app.schemas.common import SuccessResponse
from app.schemas.production_orders import (
    ProductionOrderItemResponse,
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
    """List all production orders with sales order items, optionally filtered by status."""

    try:
        production_orders = production_service.list_production_orders(session, status=status)
        
        # Transform to response schema with items
        response_data = []
        for po in production_orders:
            # Get product names for items
            items_response = []
            if po.sales_order and po.sales_order.items:
                for item in po.sales_order.items:
                    product = session.get(Product, item.product_id)
                    items_response.append(
                        ProductionOrderItemResponse(
                            id=item.id,
                            product_id=item.product_id,
                            product_name=product.name if product else None,
                            quantity=item.quantity,
                            subtotal=item.subtotal,
                        )
                    )
            
            response_data.append(
                ProductionOrderResponse(
                    id=po.id,
                    sales_order_id=po.sales_order_id,
                    status=po.status.value,
                    start_date=po.start_date,
                    end_date=po.end_date,
                    items=items_response,
                )
            )
        
        return SuccessResponse(data=response_data)
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
