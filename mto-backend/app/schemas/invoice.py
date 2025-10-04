"""
Invoice Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models import InvoiceStatus


class InvoiceBase(BaseModel):
    """Base schema for Invoice."""
    order_id: int = Field(..., description="Order ID")
    total_amount: float = Field(..., ge=0.0, description="Total invoice amount")


class InvoiceCreate(InvoiceBase):
    """Schema for generating an invoice."""
    invoice_date: Optional[datetime] = Field(None, description="Invoice date")


class InvoiceResponse(BaseModel):
    """Schema for invoice response."""
    id: int
    order_id: int
    invoice_date: Optional[datetime]
    status: str
    total_amount: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
