"""
MTO Flow Automation API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.mto import (
    AutoProductionOrderRequest,
    AutoProductionOrderResponse,
)
from app.services import (
    get_order_by_id_service,
    generate_planned_order,
    OrderNotFoundError,
    PlannedOrderValidationError,
)


router = APIRouter(prefix="/mto", tags=["MTO Flow"])


@router.post("/auto-production-order", response_model=AutoProductionOrderResponse)
def auto_create_production_order(
    request: AutoProductionOrderRequest,
    db: Session = Depends(get_db_session)
):
    """Auto-create production order (planned orders) from sales order."""
    try:
        # Get the order
        order = get_order_by_id_service(db, request.order_id)
        
        # For each order item, create a planned order
        planned_orders_created = 0
        for item in order.items:
            planned_order_data = {
                "order_item_id": item.id,
                "order_id": order.id,
                "quantity": item.quantity,
            }
            generate_planned_order(db, planned_order_data)
            planned_orders_created += 1
        
        return {
            "message": f"Successfully created {planned_orders_created} planned orders",
            "order_id": order.id,
            "planned_orders_created": planned_orders_created,
        }
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlannedOrderValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
