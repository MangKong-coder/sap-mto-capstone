"""
Repository layer for Component entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Component


def create_component(db: Session, data: dict) -> Component:
    """
    Create a new component.

    Args:
        db: Database session
        data: Dictionary containing component data (part_code, name, cost)

    Returns:
        Created Component instance
    """
    db_component = Component(**data)
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component


def get_component_by_id(db: Session, component_id: int) -> Optional[Component]:
    """
    Retrieve a component by ID.

    Args:
        db: Database session
        component_id: Component ID

    Returns:
        Component instance if found, None otherwise
    """
    return db.query(Component).filter(Component.id == component_id).first()


def list_components(db: Session, skip: int = 0, limit: int = 10) -> List[Component]:
    """
    List components with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Component instances
    """
    return db.query(Component).offset(skip).limit(limit).all()


def update_component(db: Session, component_id: int, data: dict) -> Optional[Component]:
    """
    Update a component by ID.

    Args:
        db: Database session
        component_id: Component ID
        data: Dictionary containing fields to update

    Returns:
        Updated Component instance if found, None otherwise
    """
    db_component = get_component_by_id(db, component_id)
    if not db_component:
        return None

    for key, value in data.items():
        setattr(db_component, key, value)

    db.commit()
    db.refresh(db_component)
    return db_component


def delete_component(db: Session, component_id: int) -> bool:
    """
    Delete a component by ID.

    Args:
        db: Database session
        component_id: Component ID

    Returns:
        True if deleted, False if not found
    """
    db_component = get_component_by_id(db, component_id)
    if not db_component:
        return False

    db.delete(db_component)
    db.commit()
    return True
