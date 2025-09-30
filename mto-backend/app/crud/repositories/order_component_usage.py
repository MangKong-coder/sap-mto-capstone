"""
Repository layer for OrderComponentUsage view.
Provides read-only access to aggregated component usage data.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import OrderComponentUsage


def list_order_component_usage(db: Session, order_id: Optional[int] = None) -> List[OrderComponentUsage]:
    """
    Retrieve aggregated component usage per order from the view.

    Args:
        db: Database session
        order_id: Optional order ID to filter by

    Returns:
        List of OrderComponentUsage view records
    """
    query = db.query(OrderComponentUsage)
    
    if order_id is not None:
        query = query.filter(OrderComponentUsage.order_id == order_id)
    
    return query.all()
