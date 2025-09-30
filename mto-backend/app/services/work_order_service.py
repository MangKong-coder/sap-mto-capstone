"""
Work Order Service - Business logic for production execution.
Manages production workflow including component consumption and confirmation.
"""

from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.repositories import (
    get_work_order_by_id,
    update_work_order,
    list_work_orders,
    create_component_usage,
    get_component_by_id,
)
from app.models import WorkOrder, WorkOrderStatus, ComponentUsage


class WorkOrderServiceError(Exception):
    """Base exception for work order service errors."""
    pass


class WorkOrderValidationError(WorkOrderServiceError):
    """Raised when work order validation fails."""
    pass


class WorkOrderNotFoundError(WorkOrderServiceError):
    """Raised when work order is not found."""
    pass


class WorkOrderStateError(WorkOrderServiceError):
    """Raised when work order is in invalid state for operation."""
    pass


def start_work_order(db: Session, work_id: int) -> WorkOrder:
    """
    Start a work order by setting status to IN_PROGRESS.
    
    Args:
        db: Database session
        work_id: Work order ID
    
    Returns:
        Updated WorkOrder instance
        
    Raises:
        WorkOrderNotFoundError: If work order not found
        WorkOrderStateError: If work order cannot be started
    """
    work_order = get_work_order_by_id(db, work_id)
    if not work_order:
        raise WorkOrderNotFoundError(f"Work order with ID {work_id} not found")
    
    # Validate can start
    if work_order.status == WorkOrderStatus.IN_PROGRESS:
        raise WorkOrderStateError("Work order is already in progress")
    
    if work_order.status == WorkOrderStatus.DONE:
        raise WorkOrderStateError("Cannot start completed work order")
    
    if work_order.status == WorkOrderStatus.CANCELLED:
        raise WorkOrderStateError("Cannot start cancelled work order")
    
    try:
        update_data = {
            "status": WorkOrderStatus.IN_PROGRESS,
            "start_date": datetime.now(),
        }
        updated = update_work_order(db, work_id, update_data)
        if not updated:
            raise WorkOrderNotFoundError(f"Work order with ID {work_id} not found")
        return updated
    except IntegrityError as e:
        db.rollback()
        raise WorkOrderValidationError(f"Failed to start work order: {str(e)}")


def confirm_work_order(db: Session, work_id: int, produced_qty: float) -> WorkOrder:
    """
    Confirm work order completion.
    
    Note: In a full implementation, this would also update product inventory.
    Currently, the Product model doesn't have a stock field.
    
    Args:
        db: Database session
        work_id: Work order ID
        produced_qty: Actual quantity produced
    
    Returns:
        Updated WorkOrder instance
        
    Raises:
        WorkOrderNotFoundError: If work order not found
        WorkOrderValidationError: If validation fails
        WorkOrderStateError: If work order cannot be confirmed
    """
    work_order = get_work_order_by_id(db, work_id)
    if not work_order:
        raise WorkOrderNotFoundError(f"Work order with ID {work_id} not found")
    
    # Validate can confirm
    if work_order.status == WorkOrderStatus.PENDING:
        raise WorkOrderStateError("Cannot confirm work order that hasn't started")
    
    if work_order.status == WorkOrderStatus.DONE:
        raise WorkOrderStateError("Work order is already completed")
    
    if work_order.status == WorkOrderStatus.CANCELLED:
        raise WorkOrderStateError("Cannot confirm cancelled work order")
    
    if produced_qty <= 0:
        raise WorkOrderValidationError("Produced quantity must be positive")
    
    try:
        # Update work order
        update_data = {
            "status": WorkOrderStatus.DONE,
            "end_date": datetime.now(),
            "quantity": produced_qty,  # Update with actual produced quantity
        }
        updated = update_work_order(db, work_id, update_data)
        if not updated:
            raise WorkOrderNotFoundError(f"Work order with ID {work_id} not found")
        
        # TODO: Update product inventory once stock tracking is implemented
        # This would involve:
        # 1. Get the product from order_item
        # 2. Increment product stock by produced_qty
        
        return updated
    except IntegrityError as e:
        db.rollback()
        raise WorkOrderValidationError(f"Failed to confirm work order: {str(e)}")


def consume_components(
    db: Session,
    work_id: int,
    components: List[Dict[str, Any]]
) -> List[ComponentUsage]:
    """
    Record component consumption for a work order.
    
    Args:
        db: Database session
        work_id: Work order ID
        components: List of dicts with keys: component_id, quantity
    
    Returns:
        List of created ComponentUsage instances
        
    Raises:
        WorkOrderNotFoundError: If work order not found
        WorkOrderValidationError: If validation fails
    """
    work_order = get_work_order_by_id(db, work_id)
    if not work_order:
        raise WorkOrderNotFoundError(f"Work order with ID {work_id} not found")
    
    if not components or len(components) == 0:
        raise WorkOrderValidationError("Must specify at least one component")
    
    created_usages = []
    
    try:
        for comp in components:
            if "component_id" not in comp:
                raise WorkOrderValidationError("Each component must have component_id")
            
            component_id = comp["component_id"]
            quantity = comp.get("quantity", 1.0)
            
            # Validate component exists
            component = get_component_by_id(db, component_id)
            if not component:
                raise WorkOrderValidationError(f"Component with ID {component_id} not found")
            
            if quantity <= 0:
                raise WorkOrderValidationError(f"Quantity must be positive for component {component_id}")
            
            # Create component usage record
            usage_data = {
                "work_order_id": work_id,
                "component_id": component_id,
                "quantity": quantity,
            }
            usage = create_component_usage(db, usage_data)
            created_usages.append(usage)
        
        # TODO: Deduct component stock once stock tracking is implemented
        # This would involve updating Component with a stock field and decrementing it
        
        return created_usages
        
    except IntegrityError as e:
        db.rollback()
        raise WorkOrderValidationError(f"Failed to consume components: {str(e)}")


def close_work_order(db: Session, work_id: int) -> WorkOrder:
    """
    Finalize a work order after confirmation.
    
    This is an optional step that can be used to lock the work order
    from further modifications.
    
    Args:
        db: Database session
        work_id: Work order ID
    
    Returns:
        Updated WorkOrder instance
        
    Raises:
        WorkOrderNotFoundError: If work order not found
        WorkOrderStateError: If work order cannot be closed
    """
    work_order = get_work_order_by_id(db, work_id)
    if not work_order:
        raise WorkOrderNotFoundError(f"Work order with ID {work_id} not found")
    
    # Validate can close
    if work_order.status != WorkOrderStatus.DONE:
        raise WorkOrderStateError("Can only close completed work orders")
    
    # In the current implementation, DONE is the final state
    # This function is here for API completeness and future extensibility
    # You could add a CLOSED status to WorkOrderStatus enum if needed
    
    return work_order


def get_work_order_by_id_service(db: Session, work_id: int) -> WorkOrder:
    """
    Get work order by ID with error handling.
    
    Args:
        db: Database session
        work_id: Work order ID
    
    Returns:
        WorkOrder instance
        
    Raises:
        WorkOrderNotFoundError: If work order not found
    """
    work_order = get_work_order_by_id(db, work_id)
    if not work_order:
        raise WorkOrderNotFoundError(f"Work order with ID {work_id} not found")
    return work_order


def list_work_orders_service(db: Session, skip: int = 0, limit: int = 10) -> List[WorkOrder]:
    """
    List work orders with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of WorkOrder instances
    """
    return list_work_orders(db, skip=skip, limit=limit)


def get_work_order_component_usage(db: Session, work_id: int) -> List[ComponentUsage]:
    """
    Get all component usage records for a work order.
    
    Args:
        db: Database session
        work_id: Work order ID
    
    Returns:
        List of ComponentUsage instances
        
    Raises:
        WorkOrderNotFoundError: If work order not found
    """
    work_order = get_work_order_by_id(db, work_id)
    if not work_order:
        raise WorkOrderNotFoundError(f"Work order with ID {work_id} not found")
    
    return work_order.component_usages
