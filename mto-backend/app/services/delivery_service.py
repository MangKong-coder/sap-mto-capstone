"""
Delivery Service - Business logic for customer deliveries.
Manages delivery scheduling and tracking.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.repositories import (
    create_delivery,
    get_delivery_by_id,
    list_deliveries,
    update_delivery,
    get_order_by_id,
)
from app.models import Delivery, DeliveryStatus, WorkOrderStatus, OrderStatus


class DeliveryServiceError(Exception):
    """Base exception for delivery service errors."""
    pass


class DeliveryValidationError(DeliveryServiceError):
    """Raised when delivery validation fails."""
    pass


class DeliveryNotFoundError(DeliveryServiceError):
    """Raised when delivery is not found."""
    pass


def schedule_delivery(db: Session, order_id: int, quantity: float, details: Optional[Dict[str, Any]] = None) -> Delivery:
    """
    Schedule a delivery once goods are produced.
    
    Validates that work orders are complete before scheduling delivery.
    
    Args:
        db: Database session
        order_id: Order ID
        quantity: Quantity to deliver
        details: Optional additional details (delivered_at, status)
    
    Returns:
        Created Delivery instance
        
    Raises:
        DeliveryValidationError: If validation fails
    """
    # Validate order exists
    order = get_order_by_id(db, order_id)
    if not order:
        raise DeliveryValidationError(f"Order with ID {order_id} not found")
    
    # Check order is not cancelled
    if order.status == OrderStatus.CANCELLED:
        raise DeliveryValidationError("Cannot schedule delivery for cancelled order")
    
    # Validate quantity
    if quantity <= 0:
        raise DeliveryValidationError("Delivery quantity must be positive")
    
    # Check if there are any completed work orders
    completed_work_orders = []
    for item in order.items:
        for wo in item.work_orders:
            if wo.status == WorkOrderStatus.DONE:
                completed_work_orders.append(wo)
    
    if not completed_work_orders:
        raise DeliveryValidationError(
            "Cannot schedule delivery: No completed work orders found for this order"
        )
    
    # Prepare delivery data
    if details is None:
        details = {}
    
    data = {
        "order_id": order_id,
        "quantity": quantity,
        "status": details.get("status", DeliveryStatus.PENDING),
        "delivered_at": details.get("delivered_at"),
    }
    
    try:
        delivery = create_delivery(db, data)
        
        # Update order status if first delivery
        if order.status == OrderStatus.CONFIRMED or order.status == OrderStatus.NEW:
            from app.crud.repositories import update_order
            update_order(db, order_id, {"status": OrderStatus.CONFIRMED})
        
        return delivery
    except IntegrityError as e:
        db.rollback()
        raise DeliveryValidationError(f"Failed to schedule delivery: {str(e)}")


def update_delivery_status(
    db: Session,
    delivery_id: int,
    status: DeliveryStatus,
    delivered_at: Optional[datetime] = None
) -> Delivery:
    """
    Update delivery status to track logistics.
    
    Args:
        db: Database session
        delivery_id: Delivery ID
        status: New delivery status
        delivered_at: Optional delivery timestamp
    
    Returns:
        Updated Delivery instance
        
    Raises:
        DeliveryNotFoundError: If delivery not found
        DeliveryValidationError: If validation fails
    """
    delivery = get_delivery_by_id(db, delivery_id)
    if not delivery:
        raise DeliveryNotFoundError(f"Delivery with ID {delivery_id} not found")
    
    # Validate status transition
    if delivery.status == DeliveryStatus.CANCELLED:
        raise DeliveryValidationError("Cannot update cancelled delivery")
    
    if delivery.status == DeliveryStatus.DELIVERED and status != DeliveryStatus.DELIVERED:
        raise DeliveryValidationError("Cannot change status of delivered shipment")
    
    # Prepare update data
    update_data = {"status": status}
    
    # Set delivered_at timestamp when marking as delivered
    if status == DeliveryStatus.DELIVERED:
        update_data["delivered_at"] = delivered_at or datetime.now()
    
    try:
        updated = update_delivery(db, delivery_id, update_data)
        if not updated:
            raise DeliveryNotFoundError(f"Delivery with ID {delivery_id} not found")
        
        # If delivery is complete, update order status
        if status == DeliveryStatus.DELIVERED:
            order = delivery.order
            # Check if all items are delivered (simplified logic)
            all_delivered = all(
                d.status == DeliveryStatus.DELIVERED 
                for d in order.deliveries
            )
            if all_delivered and order.status != OrderStatus.COMPLETED:
                from app.crud.repositories import update_order
                update_order(db, order.id, {"status": OrderStatus.COMPLETED})
        
        return updated
    except IntegrityError as e:
        db.rollback()
        raise DeliveryValidationError(f"Failed to update delivery: {str(e)}")


def get_customer_deliveries(db: Session, customer_id: int) -> List[Delivery]:
    """
    Fetch delivery history for a customer.
    
    Args:
        db: Database session
        customer_id: Customer ID
    
    Returns:
        List of Delivery instances
    """
    from app.models import Order, Customer
    
    # Get all orders for this customer
    orders = db.query(Order).filter(Order.customer_id == customer_id).all()
    
    # Collect all deliveries from these orders
    deliveries = []
    for order in orders:
        deliveries.extend(order.deliveries)
    
    return deliveries


def get_delivery_by_id_service(db: Session, delivery_id: int) -> Delivery:
    """
    Get delivery by ID with error handling.
    
    Args:
        db: Database session
        delivery_id: Delivery ID
    
    Returns:
        Delivery instance
        
    Raises:
        DeliveryNotFoundError: If delivery not found
    """
    delivery = get_delivery_by_id(db, delivery_id)
    if not delivery:
        raise DeliveryNotFoundError(f"Delivery with ID {delivery_id} not found")
    return delivery


def list_deliveries_service(db: Session, skip: int = 0, limit: int = 10) -> List[Delivery]:
    """
    List deliveries with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of Delivery instances
    """
    return list_deliveries(db, skip=skip, limit=limit)


def list_deliveries_by_order(db: Session, order_id: int) -> List[Delivery]:
    """
    List all deliveries for a specific order.
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        List of Delivery instances
        
    Raises:
        DeliveryValidationError: If order not found
    """
    order = get_order_by_id(db, order_id)
    if not order:
        raise DeliveryValidationError(f"Order with ID {order_id} not found")
    
    return order.deliveries
