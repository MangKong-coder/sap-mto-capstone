"""
Repository layer for OrderItem entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import OrderItem


def create_order_item(db: Session, data: dict) -> OrderItem:
    """
    Create a new order item.

    Args:
        db: Database session
        data: Dictionary containing order item data (order_id, product_id, quantity, unit_price)

    Returns:
        Created OrderItem instance
    """
    db_order_item = OrderItem(**data)
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item


def get_order_item_by_id(db: Session, item_id: int) -> Optional[OrderItem]:
    """
    Retrieve an order item by ID.

    Args:
        db: Database session
        item_id: OrderItem ID

    Returns:
        OrderItem instance if found, None otherwise
    """
    return db.query(OrderItem).filter(OrderItem.id == item_id).first()


def list_order_items(db: Session, skip: int = 0, limit: int = 10) -> List[OrderItem]:
    """
    List order items with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of OrderItem instances
    """
    return db.query(OrderItem).offset(skip).limit(limit).all()


def update_order_item(db: Session, item_id: int, data: dict) -> Optional[OrderItem]:
    """
    Update an order item by ID.

    Args:
        db: Database session
        item_id: OrderItem ID
        data: Dictionary containing fields to update

    Returns:
        Updated OrderItem instance if found, None otherwise
    """
    db_order_item = get_order_item_by_id(db, item_id)
    if not db_order_item:
        return None

    for key, value in data.items():
        setattr(db_order_item, key, value)

    db.commit()
    db.refresh(db_order_item)
    return db_order_item


def delete_order_item(db: Session, item_id: int) -> bool:
    """
    Delete an order item by ID.

    Args:
        db: Database session
        item_id: OrderItem ID

    Returns:
        True if deleted, False if not found
    """
    db_order_item = get_order_item_by_id(db, item_id)
    if not db_order_item:
        return False

    db.delete(db_order_item)
    db.commit()
    return True
