"""
Repository layer for Order entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Order


def create_order(db: Session, data: dict) -> Order:
    """
    Create a new order.

    Args:
        db: Database session
        data: Dictionary containing order data (customer_id, status, order_date, delivery_date)

    Returns:
        Created Order instance
    """
    db_order = Order(**data)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
    """
    Retrieve an order by ID.

    Args:
        db: Database session
        order_id: Order ID

    Returns:
        Order instance if found, None otherwise
    """
    return db.query(Order).filter(Order.id == order_id).first()


def list_orders(db: Session, skip: int = 0, limit: int = 10) -> List[Order]:
    """
    List orders with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Order instances
    """
    return db.query(Order).offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, data: dict) -> Optional[Order]:
    """
    Update an order by ID.

    Args:
        db: Database session
        order_id: Order ID
        data: Dictionary containing fields to update

    Returns:
        Updated Order instance if found, None otherwise
    """
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None

    for key, value in data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int) -> bool:
    """
    Delete an order by ID.

    Args:
        db: Database session
        order_id: Order ID

    Returns:
        True if deleted, False if not found
    """
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return False

    db.delete(db_order)
    db.commit()
    return True
