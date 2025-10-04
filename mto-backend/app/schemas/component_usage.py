"""
Component Usage Pydantic schemas for request/response validation.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class ComponentUsageBase(BaseModel):
    """Base schema for Component Usage."""
    work_order_id: int = Field(..., description="Work order ID")
    component_id: int = Field(..., description="Component ID")
    quantity: float = Field(..., gt=0.0, description="Quantity used")


class ComponentUsageCreate(ComponentUsageBase):
    """Schema for creating component usage record."""
    pass


class ComponentUsageResponse(ComponentUsageBase):
    """Schema for component usage response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ComponentUsageSummaryResponse(BaseModel):
    """Schema for component usage summary."""
    component_id: int
    part_code: str
    component_name: str
    total_quantity: float
    usage_count: int
    
    class Config:
        from_attributes = True
