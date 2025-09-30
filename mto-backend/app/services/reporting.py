"""
Reporting Service - Analytics and reporting functionality.
"""

from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import SalesOrder, OrderStatus, ProductionOrder, ProductionStatus, Delivery, DeliveryStatus


def get_order_summary(db: Session) -> Dict[str, Any]:
    """
    Get summary statistics for orders.
    """
    sales_count = db.query(func.count(SalesOrder.id)).scalar()
    production_count = db.query(func.count(ProductionOrder.id)).scalar()
    delivery_count = db.query(func.count(Delivery.id)).scalar()
    
    return {
        "sales_orders": {
            "total": sales_count,
            "pending": db.query(func.count(SalesOrder.id)).filter(SalesOrder.status == OrderStatus.PENDING).scalar(),
            "in_progress": db.query(func.count(SalesOrder.id)).filter(SalesOrder.status == OrderStatus.IN_PROGRESS).scalar(),
            "completed": db.query(func.count(SalesOrder.id)).filter(SalesOrder.status == OrderStatus.COMPLETED).scalar()
        },
        "production_orders": {
            "total": production_count,
            "planned": db.query(func.count(ProductionOrder.id)).filter(ProductionOrder.status == ProductionStatus.PLANNED).scalar(),
            "in_progress": db.query(func.count(ProductionOrder.id)).filter(ProductionOrder.status == ProductionStatus.IN_PROGRESS).scalar(),
            "completed": db.query(func.count(ProductionOrder.id)).filter(ProductionOrder.status == ProductionStatus.COMPLETED).scalar()
        },
        "deliveries": {
            "total": delivery_count,
            "pending": db.query(func.count(Delivery.id)).filter(Delivery.status == DeliveryStatus.PENDING).scalar(),
            "in_transit": db.query(func.count(Delivery.id)).filter(Delivery.status == DeliveryStatus.IN_TRANSIT).scalar(),
            "delivered": db.query(func.count(Delivery.id)).filter(Delivery.status == DeliveryStatus.DELIVERED).scalar()
        }
    }

