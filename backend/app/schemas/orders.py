"""Pydantic schemas for order-related API endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models import SalesOrderStatus


class OrderItemPayload(BaseModel):
    """Request payload for an order item when creating orders."""

    product_id: int
    quantity: int = Field(gt=0)


class OrderCreateRequest(BaseModel):
    """Request schema for creating a new sales order."""

    customer_id: int
    items: List[OrderItemPayload]


class OrderStatusUpdateRequest(BaseModel):
    """Request schema for updating the status of a sales order."""

    status: SalesOrderStatus


class OrderItemResponse(BaseModel):
    """Response payload for an order item."""

    id: int
    product_id: int
    product_name: Optional[str] = None
    quantity: int
    subtotal: float


class ProductionOrderResponse(BaseModel):
    """Response payload for a production order in the order details view."""

    id: int
    status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class DeliveryResponse(BaseModel):
    """Response payload for delivery information in the order details view."""

    id: int
    status: str
    delivery_date: Optional[datetime] = None


class BillingResponse(BaseModel):
    """Response payload for billing information in the order details view."""

    id: int
    invoice_number: Optional[str] = None
    amount: float
    billed_date: Optional[datetime] = None


class OrderSummaryResponse(BaseModel):
    """Summary response for orders listing."""

    id: int
    customer_name: Optional[str]
    status: SalesOrderStatus
    total_amount: float
    created_at: datetime


class OrderDetailResponse(BaseModel):
    """Detailed response model for a sales order."""

    id: int
    customer_id: int
    customer_name: Optional[str]
    status: SalesOrderStatus
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse]
    production_orders: List[ProductionOrderResponse]
    deliveries: List[DeliveryResponse]
    billing: Optional[BillingResponse] = None
