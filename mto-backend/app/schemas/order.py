"""
Order Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from app.models import OrderStatus


class OrderItemCreate(BaseModel):
    """Schema for creating an order item."""
    product_id: int = Field(..., description="Product ID")
    quantity: float = Field(..., gt=0.0, description="Quantity ordered")
    unit_price: Optional[float] = Field(None, ge=0.0, description="Unit price (optional)")


class OrderItemResponse(BaseModel):
    """Schema for order item response."""
    id: int
    order_id: int
    product_id: int
    quantity: float
    unit_price: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for placing a new order."""
    customer_id: int = Field(..., description="Customer ID")
    items: List[Dict[str, Any]] = Field(..., min_items=1, description="Order items")


class OrderResponse(BaseModel):
    """Schema for order response."""
    id: int
    customer_id: int
    status: str
    order_date: datetime
    delivery_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrderDetailResponse(OrderResponse):
    """Schema for detailed order response with items."""
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


class OrderStatusResponse(BaseModel):
    """Schema for order status response."""
    order_id: int
    status: str
    order_date: Optional[str]
    delivery_date: Optional[str]
    customer_id: int
    items_count: int
    work_orders: List[Dict[str, Any]]
    deliveries: List[Dict[str, Any]]
    invoices: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True
