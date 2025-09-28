from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from decimal import Decimal
from app.models import OrderStatus
from app.schemas.customers import CustomerResponse

class SalesOrderItemCreate(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: float = Field(..., gt=0, description="Quantity")
    unit_price: Optional[float] = Field(None, ge=0, description="Unit price")

class SalesOrderItemResponse(BaseModel):
    id: int
    line_no: int
    product_id: int
    quantity: float
    unit_price: float
    bom_id: Optional[int]
    routing_id: Optional[int]

    class Config:
        from_attributes = True

class SalesOrderCreate(BaseModel):
    customer_id: int = Field(..., description="Customer ID")
    due_date: Optional[datetime] = Field(None, description="Due date")
    notes: Optional[str] = Field(None, description="Notes")
    items: List[SalesOrderItemCreate] = Field(..., min_length=1, description="Order items")

class SalesOrderUpdate(BaseModel):
    status: Optional[OrderStatus] = Field(None, description="Order status")
    due_date: Optional[datetime] = Field(None, description="Due date")
    notes: Optional[str] = Field(None, description="Notes")

class SalesOrderSummaryResponse(BaseModel):
    id: int
    order_no: str
    customer: CustomerResponse
    status: OrderStatus
    order_date: datetime
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True

class SalesOrderResponse(SalesOrderSummaryResponse):
    items: List[SalesOrderItemResponse]

class SalesOrderListResponse(BaseModel):
    sales_orders: List[SalesOrderSummaryResponse]
    total: int
    page: int
    size: int
    pages: int

