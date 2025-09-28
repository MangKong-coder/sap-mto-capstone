from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class CustomerBase(BaseModel):
    name: str = Field(..., max_length=150, description="Customer name")
    code: Optional[str] = Field(None, max_length=32, description="Customer code")
    email: Optional[str] = Field(None, max_length=254, description="Email")
    phone: Optional[str] = Field(None, max_length=32, description="Phone")
    address_line1: Optional[str] = Field(None, max_length=200, description="Address line 1")
    address_line2: Optional[str] = Field(None, max_length=200, description="Address line 2")
    city: Optional[str] = Field(None, max_length=100, description="City")
    region: Optional[str] = Field(None, max_length=100, description="Region/State")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal code")
    country: Optional[str] = Field(None, max_length=2, description="Country code (ISO 3166-1 alpha-2)")

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CustomerListResponse(BaseModel):
    customers: List[CustomerResponse]
    total: int
    page: int
    size: int
    pages: int
