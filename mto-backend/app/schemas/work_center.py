"""
Work Center Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WorkCenterCreate(BaseModel):
    """Schema for creating a work center."""
    name: str = Field(..., min_length=1, max_length=100, description="Work center name")
    description: Optional[str] = Field(None, description="Work center description")
    address: Optional[str] = Field(None, description="Work center address")


class WorkCenterResponse(BaseModel):
    """Schema for work center response."""
    id: int
    name: str
    description: Optional[str]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
