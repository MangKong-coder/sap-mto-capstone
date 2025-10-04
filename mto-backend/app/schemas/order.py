"""
Order Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from app.models import OrderStatus, OrderPriorities


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


class OrderItemWithProduct(BaseModel):
    """Schema for order item with product details."""
    id: int
    product_id: int
    product_sku: str
    product_name: str
    quantity: float
    unit_price: float
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for placing a new order."""
    customer_id: int = Field(..., description="Customer ID")
    delivery_date: Optional[datetime] = Field(None, description="Requested delivery date")
    priority: Optional[str] = Field("STANDARD", description="Order priority")
    work_center_id: int = Field(..., description="Work center (plant/bookstore) ID")
    items: List[Dict[str, Any]] = Field(..., min_items=1, description="Order items")


class OrderResponse(BaseModel):
    """Schema for order response."""
    id: int
    customer_id: int
    status: str
    order_date: datetime
    delivery_date: Optional[datetime]
    priority: str
    work_center_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrderDetailResponse(OrderResponse):
    """Schema for detailed order response with items."""
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


class OrderEnrichedResponse(BaseModel):
    """Schema for enriched order response with customer and product details."""
    id: int
    customer_id: int
    customer_name: str
    customer_type: str
    status: str
    order_date: datetime
    delivery_date: Optional[datetime]
    priority: str
    work_center_id: int
    work_center_name: str
    items: List[OrderItemWithProduct]
    total_quantity: float
    net_value: float
    created_at: datetime
    updated_at: datetime
    
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
