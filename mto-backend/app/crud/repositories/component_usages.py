"""
Repository layer for ComponentUsage entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import ComponentUsage


def create_component_usage(db: Session, data: dict) -> ComponentUsage:
    """
    Create a new component usage record.

    Args:
        db: Database session
        data: Dictionary containing component usage data (work_order_id, component_id, quantity)

    Returns:
        Created ComponentUsage instance
    """
    db_component_usage = ComponentUsage(**data)
    db.add(db_component_usage)
    db.commit()
    db.refresh(db_component_usage)
    return db_component_usage


def get_component_usage_by_id(db: Session, usage_id: int) -> Optional[ComponentUsage]:
    """
    Retrieve a component usage record by ID.

    Args:
        db: Database session
        usage_id: ComponentUsage ID

    Returns:
        ComponentUsage instance if found, None otherwise
    """
    return db.query(ComponentUsage).filter(ComponentUsage.id == usage_id).first()


def list_component_usages(db: Session, skip: int = 0, limit: int = 10) -> List[ComponentUsage]:
    """
    List component usage records with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of ComponentUsage instances
    """
    return db.query(ComponentUsage).offset(skip).limit(limit).all()


def update_component_usage(db: Session, usage_id: int, data: dict) -> Optional[ComponentUsage]:
    """
    Update a component usage record by ID.

    Args:
        db: Database session
        usage_id: ComponentUsage ID
        data: Dictionary containing fields to update

    Returns:
        Updated ComponentUsage instance if found, None otherwise
    """
    db_component_usage = get_component_usage_by_id(db, usage_id)
    if not db_component_usage:
        return None

    for key, value in data.items():
        setattr(db_component_usage, key, value)

    db.commit()
    db.refresh(db_component_usage)
    return db_component_usage


def delete_component_usage(db: Session, usage_id: int) -> bool:
    """
    Delete a component usage record by ID.

    Args:
        db: Database session
        usage_id: ComponentUsage ID

    Returns:
        True if deleted, False if not found
    """
    db_component_usage = get_component_usage_by_id(db, usage_id)
    if not db_component_usage:
        return False

    db.delete(db_component_usage)
    db.commit()
    return True
