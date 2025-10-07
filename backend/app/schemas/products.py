"""Pydantic schemas for product API endpoints."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ProductCreateRequest(BaseModel):
    """Request payload for creating a new product."""

    name: str
    description: str
    price: float = Field(gt=0)
    stock_qty: Optional[int] = Field(default=0, ge=0)
    image_url: Optional[str] = None


class ProductResponse(BaseModel):
    """Response payload describing a product."""

    id: int
    name: str
    description: str
    price: float
    stock_qty: Optional[int] = 0
    image_url: Optional[str] = None
