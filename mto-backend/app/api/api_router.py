"""
Main API Router that aggregates all domain-specific routers.
"""

from fastapi import APIRouter

from app.api.routes import (
    components,
    component_usage,
    customers,
    orders,
    planned_orders,
    work_orders,
    deliveries,
    invoices,
    products,
    reporting,
    mto,
)


api_router = APIRouter()

# Include all domain routers
api_router.include_router(components.router)
api_router.include_router(component_usage.router)
api_router.include_router(customers.router)
api_router.include_router(orders.router)
api_router.include_router(planned_orders.router)
api_router.include_router(work_orders.router)
api_router.include_router(deliveries.router)
api_router.include_router(invoices.router)
api_router.include_router(products.router)
api_router.include_router(reporting.router)
api_router.include_router(mto.router)
