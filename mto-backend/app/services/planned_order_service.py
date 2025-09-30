"""
Planned Order Service - Business logic for production planning.
Coordinates planning from sales to production with conversion logic.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.repositories import (
    create_planned_order,
    get_planned_order_by_id,
    list_planned_orders,
    update_planned_order,
    get_order_item_by_id,
    get_order_by_id,
    create_work_order,
)
from app.models import PlannedOrder, PlannedOrderStatus, WorkOrder, WorkOrderStatus


class PlannedOrderServiceError(Exception):
    """Base exception for planned order service errors."""
    pass


class PlannedOrderValidationError(PlannedOrderServiceError):
    """Raised when planned order validation fails."""
    pass


class PlannedOrderNotFoundError(PlannedOrderServiceError):
    """Raised when planned order is not found."""
    pass


class ConversionError(PlannedOrderServiceError):
    """Raised when conversion to work order fails."""
    pass


def generate_planned_order(db: Session, order_item_id: int, quantity: Optional[float] = None) -> PlannedOrder:
    """
    Auto-generate a planned order from an order item.
    
    Args:
        db: Database session
        order_item_id: Order item ID
        quantity: Planned quantity (defaults to order item quantity)
    
    Returns:
        Created PlannedOrder instance
        
    Raises:
        PlannedOrderValidationError: If validation fails
    """
    # Validate order item exists
    order_item = get_order_item_by_id(db, order_item_id)
    if not order_item:
        raise PlannedOrderValidationError(f"Order item with ID {order_item_id} not found")
    
    # Use order item quantity if not specified
    if quantity is None:
        quantity = order_item.quantity
    
    if quantity <= 0:
        raise PlannedOrderValidationError("Planned quantity must be positive")
    
    try:
        data = {
            "order_item_id": order_item_id,
            "order_id": order_item.order_id,
            "quantity": quantity,
            "status": PlannedOrderStatus.PLANNED,
            "planned_start": None,  # Can be set later
            "planned_end": None,
        }
        return create_planned_order(db, data)
    except IntegrityError as e:
        db.rollback()
        raise PlannedOrderValidationError(f"Failed to create planned order: {str(e)}")


def update_planned_order_status(
    db: Session,
    planned_id: int,
    status: PlannedOrderStatus,
    **kwargs
) -> PlannedOrder:
    """
    Update planned order status and optional fields.
    
    Args:
        db: Database session
        planned_id: Planned order ID
        status: New status
        **kwargs: Additional fields to update (planned_start, planned_end, quantity)
    
    Returns:
        Updated PlannedOrder instance
        
    Raises:
        PlannedOrderNotFoundError: If planned order not found
        PlannedOrderValidationError: If validation fails
    """
    planned = get_planned_order_by_id(db, planned_id)
    if not planned:
        raise PlannedOrderNotFoundError(f"Planned order with ID {planned_id} not found")
    
    # Validate status transition
    if planned.status == PlannedOrderStatus.CONVERTED and status != PlannedOrderStatus.CONVERTED:
        raise PlannedOrderValidationError("Cannot change status of converted planned order")
    
    if planned.status == PlannedOrderStatus.CANCELLED:
        raise PlannedOrderValidationError("Cannot change status of cancelled planned order")
    
    # Prepare update data
    update_data = {"status": status}
    
    # Add optional fields
    if "quantity" in kwargs:
        if kwargs["quantity"] <= 0:
            raise PlannedOrderValidationError("Quantity must be positive")
        update_data["quantity"] = kwargs["quantity"]
    
    if "planned_start" in kwargs:
        update_data["planned_start"] = kwargs["planned_start"]
    
    if "planned_end" in kwargs:
        update_data["planned_end"] = kwargs["planned_end"]
    
    try:
        updated = update_planned_order(db, planned_id, update_data)
        if not updated:
            raise PlannedOrderNotFoundError(f"Planned order with ID {planned_id} not found")
        return updated
    except IntegrityError as e:
        db.rollback()
        raise PlannedOrderValidationError(f"Failed to update planned order: {str(e)}")


def convert_to_work_order(db: Session, planned_id: int) -> WorkOrder:
    """
    Convert a planned order to a work order.
    
    Args:
        db: Database session
        planned_id: Planned order ID
    
    Returns:
        Created WorkOrder instance
        
    Raises:
        PlannedOrderNotFoundError: If planned order not found
        ConversionError: If conversion fails
    """
    planned = get_planned_order_by_id(db, planned_id)
    if not planned:
        raise PlannedOrderNotFoundError(f"Planned order with ID {planned_id} not found")
    
    # Validate can convert
    if planned.status == PlannedOrderStatus.CONVERTED:
        raise ConversionError("Planned order already converted")
    
    if planned.status == PlannedOrderStatus.CANCELLED:
        raise ConversionError("Cannot convert cancelled planned order")
    
    # Check if work order already exists
    if planned.work_order:
        raise ConversionError(f"Work order {planned.work_order.id} already exists for this planned order")
    
    try:
        # Create work order
        work_order_data = {
            "planned_order_id": planned.id,
            "order_item_id": planned.order_item_id,
            "quantity": planned.quantity,
            "status": WorkOrderStatus.PENDING,
            "start_date": None,
            "end_date": None,
        }
        work_order = create_work_order(db, work_order_data)
        
        # Update planned order status
        update_planned_order(db, planned_id, {"status": PlannedOrderStatus.CONVERTED})
        
        return work_order
    except IntegrityError as e:
        db.rollback()
        raise ConversionError(f"Failed to convert to work order: {str(e)}")


def get_planned_order_by_id_service(db: Session, planned_id: int) -> PlannedOrder:
    """
    Get planned order by ID with error handling.
    
    Args:
        db: Database session
        planned_id: Planned order ID
    
    Returns:
        PlannedOrder instance
        
    Raises:
        PlannedOrderNotFoundError: If planned order not found
    """
    planned = get_planned_order_by_id(db, planned_id)
    if not planned:
        raise PlannedOrderNotFoundError(f"Planned order with ID {planned_id} not found")
    return planned


def list_planned_orders_service(db: Session, skip: int = 0, limit: int = 10) -> List[PlannedOrder]:
    """
    List planned orders with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of PlannedOrder instances
    """
    return list_planned_orders(db, skip=skip, limit=limit)


def list_planned_orders_by_order(db: Session, order_id: int) -> List[PlannedOrder]:
    """
    List all planned orders for a specific order.
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        List of PlannedOrder instances
    """
    order = get_order_by_id(db, order_id)
    if not order:
        raise PlannedOrderValidationError(f"Order with ID {order_id} not found")
    
    return db.query(PlannedOrder).filter(PlannedOrder.order_id == order_id).all()
