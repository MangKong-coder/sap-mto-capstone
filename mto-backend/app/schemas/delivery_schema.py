"""
Delivery Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models import DeliveryStatus


class DeliveryBase(BaseModel):
    """Base schema for Delivery."""
    order_id: int = Field(..., description="Order ID")
    quantity: float = Field(..., gt=0.0, description="Delivery quantity")


class DeliveryCreate(DeliveryBase):
    """Schema for scheduling a delivery."""
    delivered_at: Optional[datetime] = Field(None, description="Delivery date")


class DeliveryStatusUpdate(BaseModel):
    """Schema for updating delivery status."""
    status: DeliveryStatus = Field(..., description="New delivery status")
    delivered_at: Optional[datetime] = Field(None, description="Actual delivery date")


class DeliveryResponse(BaseModel):
    """Schema for delivery response."""
    id: int
    order_id: int
    delivered_at: Optional[datetime]
    status: str
    quantity: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
