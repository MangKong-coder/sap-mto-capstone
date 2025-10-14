# Production order schemas

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ProductionOrderStartRequest(BaseModel):

    sales_order_id: int


class ProductionOrderItemResponse(BaseModel):

    id: int
    product_id: int
    product_name: Optional[str] = None
    quantity: int
    subtotal: float


class ProductionOrderResponse(BaseModel):

    id: int
    sales_order_id: int
    status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    items: List[ProductionOrderItemResponse] = []
