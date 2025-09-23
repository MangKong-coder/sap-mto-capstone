from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .sales import ProductResponse


class InventoryBase(BaseModel):
    product_id: int
    quantity: int = 0


class InventoryResponse(InventoryBase):
    id: int
    product: Optional[ProductResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
