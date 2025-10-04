"""
Reporting Pydantic schemas for request/response validation.
"""

from typing import List, Dict, Any
from pydantic import BaseModel


class OrderFlowResponse(BaseModel):
    """Schema for order flow trace response."""
    order_id: int
    order_status: str
    customer_name: str
    planned_orders: List[Dict[str, Any]]
    work_orders: List[Dict[str, Any]]
    deliveries: List[Dict[str, Any]]
    invoices: List[Dict[str, Any]]
    component_usage: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True


class ProductionStatusSummaryResponse(BaseModel):
    """Schema for production status summary."""
    total_work_orders: int
    pending: int
    in_progress: int
    done: int
    cancelled: int
    
    class Config:
        from_attributes = True


class ComponentConsumptionResponse(BaseModel):
    """Schema for component consumption summary."""
    component_id: int
    part_code: str
    component_name: str
    total_consumed: float
    usage_count: int
    total_cost: float
    
    class Config:
        from_attributes = True


class OrderComponentUsageResponse(BaseModel):
    """Schema for order component usage."""
    order_id: int
    components: List[Dict[str, Any]]
    total_cost: float
    
    class Config:
        from_attributes = True


class CustomerSummaryResponse(BaseModel):
    """Schema for customer order summary."""
    customer_id: int
    customer_name: str
    total_orders: int
    total_spent: float
    orders: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True
