"""
Repository layer for Delivery entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Delivery


def create_delivery(db: Session, data: dict) -> Delivery:
    """
    Create a new delivery record.

    Args:
        db: Database session
        data: Dictionary containing delivery data (order_id, delivered_at, status, quantity)

    Returns:
        Created Delivery instance
    """
    db_delivery = Delivery(**data)
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery


def get_delivery_by_id(db: Session, delivery_id: int) -> Optional[Delivery]:
    """
    Retrieve a delivery by ID.

    Args:
        db: Database session
        delivery_id: Delivery ID

    Returns:
        Delivery instance if found, None otherwise
    """
    return db.query(Delivery).filter(Delivery.id == delivery_id).first()


def list_deliveries(db: Session, skip: int = 0, limit: int = 10) -> List[Delivery]:
    """
    List deliveries with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Delivery instances
    """
    return db.query(Delivery).offset(skip).limit(limit).all()


def update_delivery(db: Session, delivery_id: int, data: dict) -> Optional[Delivery]:
    """
    Update a delivery by ID.

    Args:
        db: Database session
        delivery_id: Delivery ID
        data: Dictionary containing fields to update

    Returns:
        Updated Delivery instance if found, None otherwise
    """
    db_delivery = get_delivery_by_id(db, delivery_id)
    if not db_delivery:
        return None

    for key, value in data.items():
        setattr(db_delivery, key, value)

    db.commit()
    db.refresh(db_delivery)
    return db_delivery


def delete_delivery(db: Session, delivery_id: int) -> bool:
    """
    Delete a delivery by ID.

    Args:
        db: Database session
        delivery_id: Delivery ID

    Returns:
        True if deleted, False if not found
    """
    db_delivery = get_delivery_by_id(db, delivery_id)
    if not db_delivery:
        return False

    db.delete(db_delivery)
    db.commit()
    return True
