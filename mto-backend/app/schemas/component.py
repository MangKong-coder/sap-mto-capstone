"""
Component Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ComponentBase(BaseModel):
    """Base schema for Component."""
    part_code: str = Field(..., min_length=1, max_length=50, description="Unique part code")
    name: str = Field(..., min_length=1, max_length=100, description="Component name")
    cost: float = Field(..., ge=0.0, description="Component cost")


class ComponentCreate(ComponentBase):
    """Schema for creating a new component."""
    pass


class ComponentUpdate(BaseModel):
    """Schema for updating component details."""
    part_code: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    cost: Optional[float] = Field(None, ge=0.0)


class ComponentResponse(ComponentBase):
    """Schema for component response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ComponentAvailabilityResponse(BaseModel):
    """Schema for component availability check."""
    component_id: int
    part_code: str
    name: str
    cost: float
    total_consumed: float
    note: str
    
    class Config:
        from_attributes = True
