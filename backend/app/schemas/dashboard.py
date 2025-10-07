"""Pydantic schemas for dashboard API endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel


class TopProductResponse(BaseModel):
    """Response payload for top products in dashboard."""

    product_id: int
    name: str | None
    orders: int


class RecentOrderResponse(BaseModel):
    """Response payload for recent orders in dashboard."""

    id: int
    customer_name: str
    status: str
    total_amount: float
    created_at: datetime


class DashboardSummaryResponse(BaseModel):
    """Response payload for dashboard summary."""

    total_orders: int
    in_production: int
    ready_for_delivery: int
    billed: int
    top_products: List[TopProductResponse]
    recent_orders: List[RecentOrderResponse]
