"""
Customer Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class CustomerBase(BaseModel):
    """Base schema for Customer."""
    name: str = Field(..., min_length=1, max_length=100, description="Customer name")
    email: Optional[str] = Field(None, max_length=200, description="Customer email")
    phone: Optional[str] = Field(None, max_length=50, description="Customer phone")
    address: Optional[str] = Field(None, description="Customer address")


class CustomerCreate(CustomerBase):
    """Schema for registering a new customer."""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating customer profile."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Schema for customer response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
