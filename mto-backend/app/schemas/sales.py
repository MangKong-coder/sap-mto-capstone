from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    product: Optional[ProductResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    status: str = "pending"


class OrderCreate(OrderBase):
    items: List[OrderItemBase]


class OrderResponse(OrderBase):
    id: int
    user_id: int
    items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
