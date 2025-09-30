from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models import ProductionStatus


class ProductionOrderBase(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., gt=0)


class ProductionOrderCreate(ProductionOrderBase):
    sales_order_id: int


class ProductionOrderUpdate(BaseModel):
    status: Optional[ProductionStatus] = None
    start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None


class ProductionOrderResponse(ProductionOrderBase):
    id: int
    order_number: str
    sales_order_id: int
    status: ProductionStatus
    start_date: Optional[datetime]
    completion_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

