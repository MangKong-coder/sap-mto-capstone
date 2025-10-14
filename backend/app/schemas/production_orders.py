"""Pydantic schemas for production order API endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ProductionOrderStartRequest(BaseModel):
    """Request payload to start production for a sales order."""

    sales_order_id: int


class ProductionOrderItemResponse(BaseModel):
    """Response model for a sales order item in production order context."""

    id: int
    product_id: int
    product_name: Optional[str] = None
    quantity: int
    subtotal: float


class ProductionOrderResponse(BaseModel):
    """Response model describing a production order."""

    id: int
    sales_order_id: int
    status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    items: List[ProductionOrderItemResponse] = []
