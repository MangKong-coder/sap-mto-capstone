"""
Planned Order Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models import PlannedOrderStatus


class PlannedOrderBase(BaseModel):
    """Base schema for Planned Order."""
    order_item_id: int = Field(..., description="Order item ID")
    quantity: float = Field(..., gt=0.0, description="Planned quantity")


class PlannedOrderCreate(PlannedOrderBase):
    """Schema for generating a planned order."""
    order_id: int = Field(..., description="Order ID")
    planned_start: Optional[datetime] = Field(None, description="Planned start date")
    planned_end: Optional[datetime] = Field(None, description="Planned end date")


class PlannedOrderUpdate(BaseModel):
    """Schema for updating planned order."""
    status: Optional[PlannedOrderStatus] = None
    quantity: Optional[float] = Field(None, gt=0.0)
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None


class PlannedOrderResponse(BaseModel):
    """Schema for planned order response."""
    id: int
    order_item_id: int
    order_id: int
    quantity: float
    status: str
    planned_start: Optional[datetime]
    planned_end: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
