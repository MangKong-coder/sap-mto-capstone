from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models import OrderStatus


class SalesOrderBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=200)
    product_name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)


class SalesOrderCreate(SalesOrderBase):
    pass


class SalesOrderUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=1, max_length=200)
    product_name: Optional[str] = Field(None, min_length=1, max_length=200)
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[Decimal] = Field(None, gt=0)
    status: Optional[OrderStatus] = None


class SalesOrderResponse(SalesOrderBase):
    id: int
    order_number: str
    total_amount: Decimal
    status: OrderStatus
    order_date: datetime
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


