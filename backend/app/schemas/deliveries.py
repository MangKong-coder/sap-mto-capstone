"""Pydantic schemas for delivery API endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeliveryCreateRequest(BaseModel):
    """Request payload for creating a delivery for a sales order."""

    sales_order_id: int
    delivery_date: Optional[datetime] = None


class DeliveryResponse(BaseModel):
    """Response payload describing a delivery entry."""

    id: int
    sales_order_id: int
    status: str
    delivery_date: Optional[datetime] = None
