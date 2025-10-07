"""Pydantic schemas for production order API endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductionOrderStartRequest(BaseModel):
    """Request payload to start production for a sales order."""

    sales_order_id: int


class ProductionOrderResponse(BaseModel):
    """Response model describing a production order."""

    id: int
    sales_order_id: int
    status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
