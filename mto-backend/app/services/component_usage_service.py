"""
Component Usage Service - Business logic for tracking material consumption.
Logs and reports component usage in production.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.repositories import (
    create_component_usage,
    get_component_usage_by_id,
    list_component_usages,
    get_work_order_by_id,
    get_component_by_id,
    list_order_component_usage,
)
from app.models import ComponentUsage, OrderComponentUsage


class ComponentUsageServiceError(Exception):
    """Base exception for component usage service errors."""
    pass


class ComponentUsageValidationError(ComponentUsageServiceError):
    """Raised when component usage validation fails."""
    pass


class ComponentUsageNotFoundError(ComponentUsageServiceError):
    """Raised when component usage is not found."""
    pass


def record_component_usage(
    db: Session,
    work_id: int,
    component_id: int,
    qty_used: float
) -> ComponentUsage:
    """
    Log component usage against a work order.
    
    Args:
        db: Database session
        work_id: Work order ID
        component_id: Component ID
        qty_used: Quantity used
    
    Returns:
        Created ComponentUsage instance
        
    Raises:
        ComponentUsageValidationError: If validation fails
    """
    # Validate work order exists
    work_order = get_work_order_by_id(db, work_id)
    if not work_order:
        raise ComponentUsageValidationError(f"Work order with ID {work_id} not found")
    
    # Validate component exists
    component = get_component_by_id(db, component_id)
    if not component:
        raise ComponentUsageValidationError(f"Component with ID {component_id} not found")
    
    # Validate quantity
    if qty_used <= 0:
        raise ComponentUsageValidationError("Quantity used must be positive")
    
    try:
        data = {
            "work_order_id": work_id,
            "component_id": component_id,
            "quantity": qty_used,
        }
        return create_component_usage(db, data)
    except IntegrityError as e:
        db.rollback()
        raise ComponentUsageValidationError(f"Failed to record component usage: {str(e)}")


def get_usage_by_work_order(db: Session, work_id: int) -> List[ComponentUsage]:
    """
    Fetch all component usage for a work order.
    
    Args:
        db: Database session
        work_id: Work order ID
    
    Returns:
        List of ComponentUsage instances
        
    Raises:
        ComponentUsageValidationError: If work order not found
    """
    work_order = get_work_order_by_id(db, work_id)
    if not work_order:
        raise ComponentUsageValidationError(f"Work order with ID {work_id} not found")
    
    return db.query(ComponentUsage).filter(ComponentUsage.work_order_id == work_id).all()


def summarize_component_usage(db: Session, order_id: int) -> List[Dict[str, Any]]:
    """
    Aggregate component usage per order using the database view.
    
    This uses the vw_order_component_usage view to get aggregated data.
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        List of dictionaries with aggregated usage data
    """
    # Query the view
    view_results = list_order_component_usage(db, order_id=order_id)
    
    # Transform to dictionary format with component details
    summary = []
    for view_record in view_results:
        # Fetch component details
        component = get_component_by_id(db, view_record.component_id)
        
        summary.append({
            "order_id": view_record.order_id,
            "component_id": view_record.component_id,
            "component_name": component.name if component else "Unknown",
            "part_code": component.part_code if component else "Unknown",
            "cost": component.cost if component else 0.0,
            "total_used": view_record.total_used,
            "total_cost": (component.cost * view_record.total_used) if component else 0.0,
        })
    
    return summary


def get_component_usage_by_id_service(db: Session, usage_id: int) -> ComponentUsage:
    """
    Get component usage by ID with error handling.
    
    Args:
        db: Database session
        usage_id: Component usage ID
    
    Returns:
        ComponentUsage instance
        
    Raises:
        ComponentUsageNotFoundError: If component usage not found
    """
    usage = get_component_usage_by_id(db, usage_id)
    if not usage:
        raise ComponentUsageNotFoundError(f"Component usage with ID {usage_id} not found")
    return usage


def list_component_usages_service(
    db: Session,
    skip: int = 0,
    limit: int = 10
) -> List[ComponentUsage]:
    """
    List component usages with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of ComponentUsage instances
    """
    return list_component_usages(db, skip=skip, limit=limit)


def get_component_usage_by_component(db: Session, component_id: int) -> List[ComponentUsage]:
    """
    Get all usage records for a specific component.
    
    Args:
        db: Database session
        component_id: Component ID
    
    Returns:
        List of ComponentUsage instances
        
    Raises:
        ComponentUsageValidationError: If component not found
    """
    component = get_component_by_id(db, component_id)
    if not component:
        raise ComponentUsageValidationError(f"Component with ID {component_id} not found")
    
    return db.query(ComponentUsage).filter(ComponentUsage.component_id == component_id).all()
