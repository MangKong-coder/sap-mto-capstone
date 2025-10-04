"""
Work Order Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from app.models import WorkOrderStatus


class WorkOrderResponse(BaseModel):
    """Schema for work order response."""
    id: int
    planned_order_id: Optional[int]
    order_item_id: int
    quantity: float
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkOrderConfirmRequest(BaseModel):
    """Schema for confirming work order completion."""
    produced_qty: float = Field(..., gt=0.0, description="Actual quantity produced")


class WorkOrderConsumeRequest(BaseModel):
    """Schema for consuming components."""
    components: List[Dict[str, Any]] = Field(..., min_items=1, description="Components to consume")
