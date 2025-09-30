"""
Repository layer for PlannedOrder entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import PlannedOrder


def create_planned_order(db: Session, data: dict) -> PlannedOrder:
    """
    Create a new planned order.

    Args:
        db: Database session
        data: Dictionary containing planned order data (order_item_id, order_id, quantity, status, planned_start, planned_end)

    Returns:
        Created PlannedOrder instance
    """
    db_planned_order = PlannedOrder(**data)
    db.add(db_planned_order)
    db.commit()
    db.refresh(db_planned_order)
    return db_planned_order


def get_planned_order_by_id(db: Session, planned_id: int) -> Optional[PlannedOrder]:
    """
    Retrieve a planned order by ID.

    Args:
        db: Database session
        planned_id: PlannedOrder ID

    Returns:
        PlannedOrder instance if found, None otherwise
    """
    return db.query(PlannedOrder).filter(PlannedOrder.id == planned_id).first()


def list_planned_orders(db: Session, skip: int = 0, limit: int = 10) -> List[PlannedOrder]:
    """
    List planned orders with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of PlannedOrder instances
    """
    return db.query(PlannedOrder).offset(skip).limit(limit).all()


def update_planned_order(db: Session, planned_id: int, data: dict) -> Optional[PlannedOrder]:
    """
    Update a planned order by ID.

    Args:
        db: Database session
        planned_id: PlannedOrder ID
        data: Dictionary containing fields to update

    Returns:
        Updated PlannedOrder instance if found, None otherwise
    """
    db_planned_order = get_planned_order_by_id(db, planned_id)
    if not db_planned_order:
        return None

    for key, value in data.items():
        setattr(db_planned_order, key, value)

    db.commit()
    db.refresh(db_planned_order)
    return db_planned_order


def delete_planned_order(db: Session, planned_id: int) -> bool:
    """
    Delete a planned order by ID.

    Args:
        db: Database session
        planned_id: PlannedOrder ID

    Returns:
        True if deleted, False if not found
    """
    db_planned_order = get_planned_order_by_id(db, planned_id)
    if not db_planned_order:
        return False

    db.delete(db_planned_order)
    db.commit()
    return True
