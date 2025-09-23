from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductionOrderBase(BaseModel):
    order_id: int
    product_id: int
    planned_quantity: int
    status: str = "created"
    scheduled_date: datetime


class ProductionOrderCreate(ProductionOrderBase):
    pass


class ProductionOrderResponse(ProductionOrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkCenterBase(BaseModel):
    name: str
    capacity: int = 1


class WorkCenterCreate(WorkCenterBase):
    pass


class WorkCenterResponse(WorkCenterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoutingStepBase(BaseModel):
    product_id: int
    work_center_id: int
    step_number: int
    description: Optional[str] = None
    duration_minutes: int = 0


class RoutingStepCreate(RoutingStepBase):
    pass


class RoutingStepResponse(RoutingStepBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
