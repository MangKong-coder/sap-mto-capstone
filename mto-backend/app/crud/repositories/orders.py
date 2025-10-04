"""
Repository layer for Order entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models import Order, Customer, WorkCenter, OrderItem


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


def list_orders_with_details(db: Session, skip: int = 0, limit: int = 20) -> List[Order]:
    """
    List orders with customer, work center, and order items (with products) eagerly loaded.
    
    This function is optimized for frontend display by preloading all necessary relationships
    to avoid N+1 query problems.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Order instances with relationships loaded
    """
    return (
        db.query(Order)
        .options(
            joinedload(Order.customer),
            joinedload(Order.work_center),
            joinedload(Order.items).joinedload(OrderItem.product)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_order_with_details(db: Session, order_id: int) -> Optional[Order]:
    """
    Get a single order with all relationships loaded.

    Args:
        db: Database session
        order_id: Order ID

    Returns:
        Order instance with relationships loaded if found, None otherwise
    """
    return (
        db.query(Order)
        .options(
            joinedload(Order.customer),
            joinedload(Order.work_center),
            joinedload(Order.items).joinedload(OrderItem.product)
        )
        .filter(Order.id == order_id)
        .first()
    )
