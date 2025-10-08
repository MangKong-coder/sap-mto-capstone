"""Pydantic schemas for billing API endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BillingCreateRequest(BaseModel):
    """Request payload for generating a billing record."""

    sales_order_id: int


class BillingSendInvoiceRequest(BaseModel):
    """Request payload for generating a billing record and emailing the invoice."""

    sales_order_id: int


class BillingResponse(BaseModel):
    """Response payload describing a billing entry."""

    id: int
    sales_order_id: int
    invoice_number: Optional[str] = None
    amount: float
    billed_date: Optional[datetime] = None
