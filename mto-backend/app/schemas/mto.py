"""
MTO Flow Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field


class AutoProductionOrderRequest(BaseModel):
    """Schema for auto-creating production order from sales order."""
    order_id: int = Field(..., description="Sales order ID to create production from")


class AutoProductionOrderResponse(BaseModel):
    """Schema for auto production order response."""
    message: str
    order_id: int
    planned_orders_created: int
    
    class Config:
        from_attributes = True
