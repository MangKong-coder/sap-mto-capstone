"""
Component Service - Business logic for raw material management.
Tracks component availability and inventory.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.repositories import (
    create_component,
    get_component_by_id,
    list_components,
    update_component,
)
from app.models import Component


class ComponentServiceError(Exception):
    """Base exception for component service errors."""
    pass


class ComponentValidationError(ComponentServiceError):
    """Raised when component validation fails."""
    pass


class ComponentNotFoundError(ComponentServiceError):
    """Raised when component is not found."""
    pass


def add_component(db: Session, data: dict) -> Component:
    """
    Register a new raw material component.
    
    Args:
        db: Database session
        data: Dictionary with component data (part_code, name, cost)
    
    Returns:
        Created Component instance
        
    Raises:
        ComponentValidationError: If validation fails
    """
    # Validate required fields
    if not data.get("part_code"):
        raise ComponentValidationError("Component part_code is required")
    if not data.get("name"):
        raise ComponentValidationError("Component name is required")
    
    # Validate cost
    cost = data.get("cost", 0.0)
    if cost < 0:
        raise ComponentValidationError("Cost cannot be negative")
    
    # Check part_code uniqueness
    part_code = data["part_code"]
    existing = db.query(Component).filter(Component.part_code == part_code).first()
    if existing:
        raise ComponentValidationError(f"Component with part_code {part_code} already exists")
    
    try:
        return create_component(db, data)
    except IntegrityError as e:
        db.rollback()
        raise ComponentValidationError(f"Failed to create component: {str(e)}")


def update_component_details(db: Session, component_id: int, data: dict) -> Component:
    """
    Update component details with validation.
    
    Note: In the current schema, components don't have a stock field.
    Stock would need to be tracked separately if required.
    
    Args:
        db: Database session
        component_id: Component ID
        data: Dictionary with fields to update
    
    Returns:
        Updated Component instance
        
    Raises:
        ComponentNotFoundError: If component not found
        ComponentValidationError: If validation fails
    """
    component = get_component_by_id(db, component_id)
    if not component:
        raise ComponentNotFoundError(f"Component with ID {component_id} not found")
    
    # Validate part_code uniqueness if being updated
    if "part_code" in data:
        part_code = data["part_code"]
        if not part_code:
            raise ComponentValidationError("Component part_code cannot be empty")
        
        existing = db.query(Component).filter(
            Component.part_code == part_code,
            Component.id != component_id
        ).first()
        if existing:
            raise ComponentValidationError(f"Part code {part_code} already in use")
    
    # Validate name
    if "name" in data and not data["name"]:
        raise ComponentValidationError("Component name cannot be empty")
    
    # Validate cost
    if "cost" in data and data["cost"] < 0:
        raise ComponentValidationError("Cost cannot be negative")
    
    try:
        updated = update_component(db, component_id, data)
        if not updated:
            raise ComponentNotFoundError(f"Component with ID {component_id} not found")
        return updated
    except IntegrityError as e:
        db.rollback()
        raise ComponentValidationError(f"Failed to update component: {str(e)}")


def get_component_availability(db: Session, component_id: int) -> dict:
    """
    Check component availability.
    
    Note: In the current schema, components don't have a stock field.
    To implement proper inventory tracking, you would need to either:
    1. Add a stock/quantity field to the Component model
    2. Create a separate ComponentInventory table
    3. Calculate available stock by tracking purchases and usages
    
    Args:
        db: Database session
        component_id: Component ID
    
    Returns:
        Dictionary with component information
        
    Raises:
        ComponentNotFoundError: If component not found
    """
    component = get_component_by_id(db, component_id)
    if not component:
        raise ComponentNotFoundError(f"Component with ID {component_id} not found")
    
    # Calculate total used across all work orders
    total_used = 0.0
    for usage in component.usages:
        total_used += usage.quantity
    
    return {
        "component_id": component.id,
        "part_code": component.part_code,
        "name": component.name,
        "cost": component.cost,
        "total_consumed": total_used,
        "note": "Stock tracking not implemented in current schema"
    }


def get_component_by_part_code(db: Session, part_code: str) -> Optional[Component]:
    """
    Get component by part code.
    
    Args:
        db: Database session
        part_code: Component part code
    
    Returns:
        Component instance if found, None otherwise
    """
    return db.query(Component).filter(Component.part_code == part_code).first()


def get_component_by_id_service(db: Session, component_id: int) -> Component:
    """
    Get component by ID with error handling.
    
    Args:
        db: Database session
        component_id: Component ID
    
    Returns:
        Component instance
        
    Raises:
        ComponentNotFoundError: If component not found
    """
    component = get_component_by_id(db, component_id)
    if not component:
        raise ComponentNotFoundError(f"Component with ID {component_id} not found")
    return component


def list_components_service(db: Session, skip: int = 0, limit: int = 10) -> List[Component]:
    """
    List components with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of Component instances
    """
    return list_components(db, skip=skip, limit=limit)
