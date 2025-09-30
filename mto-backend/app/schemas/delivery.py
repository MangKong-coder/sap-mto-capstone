from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models import DeliveryStatus


class DeliveryBase(BaseModel):
    quantity: int = Field(..., gt=0)


class DeliveryCreate(DeliveryBase):
    production_order_id: int
    sales_order_id: int


class DeliveryUpdate(BaseModel):
    status: Optional[DeliveryStatus] = None
    delivery_date: Optional[datetime] = None


class DeliveryResponse(DeliveryBase):
    id: int
    delivery_number: str
    production_order_id: int
    sales_order_id: int
    status: DeliveryStatus
    delivery_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

