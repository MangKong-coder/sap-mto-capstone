"""
Repository layer for WorkOrder entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import WorkOrder


def create_work_order(db: Session, data: dict) -> WorkOrder:
    """
    Create a new work order.

    Args:
        db: Database session
        data: Dictionary containing work order data (planned_order_id, order_item_id, quantity, status, start_date, end_date)

    Returns:
        Created WorkOrder instance
    """
    db_work_order = WorkOrder(**data)
    db.add(db_work_order)
    db.commit()
    db.refresh(db_work_order)
    return db_work_order


def get_work_order_by_id(db: Session, work_id: int) -> Optional[WorkOrder]:
    """
    Retrieve a work order by ID.

    Args:
        db: Database session
        work_id: WorkOrder ID

    Returns:
        WorkOrder instance if found, None otherwise
    """
    return db.query(WorkOrder).filter(WorkOrder.id == work_id).first()


def list_work_orders(db: Session, skip: int = 0, limit: int = 10) -> List[WorkOrder]:
    """
    List work orders with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of WorkOrder instances
    """
    return db.query(WorkOrder).offset(skip).limit(limit).all()


def update_work_order(db: Session, work_id: int, data: dict) -> Optional[WorkOrder]:
    """
    Update a work order by ID.

    Args:
        db: Database session
        work_id: WorkOrder ID
        data: Dictionary containing fields to update

    Returns:
        Updated WorkOrder instance if found, None otherwise
    """
    db_work_order = get_work_order_by_id(db, work_id)
    if not db_work_order:
        return None

    for key, value in data.items():
        setattr(db_work_order, key, value)

    db.commit()
    db.refresh(db_work_order)
    return db_work_order


def delete_work_order(db: Session, work_id: int) -> bool:
    """
    Delete a work order by ID.

    Args:
        db: Database session
        work_id: WorkOrder ID

    Returns:
        True if deleted, False if not found
    """
    db_work_order = get_work_order_by_id(db, work_id)
    if not db_work_order:
        return False

    db.delete(db_work_order)
    db.commit()
    return True
