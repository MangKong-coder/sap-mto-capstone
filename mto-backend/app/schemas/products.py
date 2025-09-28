from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models import UoM


class ProductBase(BaseModel):
    name: str = Field(..., max_length=150, description="Product name")
    sku: str = Field(..., max_length=64, description="Stock Keeping Unit")
    description: Optional[str] = Field(None, description="Product description")
    unit_of_measure: UoM  = Field(..., description="Unit of measure")
    make_to_order: bool = Field(True, description="Whether product is make-to-order")
    standard_cost: float = Field(0.0, ge=0, description="Standard cost")
    list_price: float = Field(0.0, ge=0, description="List price")
    is_active: bool = Field(True, description="Whether product is active")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=150, description="Product name")
    sku: Optional[str] = Field(None, max_length=64, description="Stock Keeping Unit")
    description: Optional[str] = Field(None, description="Product description")
    unit_of_measure: Optional[UoM] = Field(None, description="Unit of measure")
    make_to_order: Optional[bool] = Field(None, description="Whether product is make-to-order")
    standard_cost: Optional[float] = Field(None, ge=0, description="Standard cost")
    list_price: Optional[float] = Field(None, ge=0, description="List price")
    is_active: Optional[bool] = Field(None, description="Whether product is active")


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int
    page: int
    size: int
    pages: int
