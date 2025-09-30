"""
Order Service - Business logic for sales order management.
Handles order lifecycle with validation, product checks, and status tracking.
"""

from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.repositories import (
    create_order,
    get_order_by_id,
    list_orders,
    update_order,
    create_order_item,
    get_customer_by_id,
    get_product_by_id,
)
from app.models import Order, OrderItem, OrderStatus, Customer


class OrderServiceError(Exception):
    """Base exception for order service errors."""
    pass


class OrderValidationError(OrderServiceError):
    """Raised when order validation fails."""
    pass


class OrderNotFoundError(OrderServiceError):
    """Raised when order is not found."""
    pass


class OrderCancellationError(OrderServiceError):
    """Raised when order cannot be cancelled."""
    pass


def place_order(db: Session, customer_id: int, items: List[Dict[str, Any]]) -> Order:
    """
    Place a new order with validation.
    
    Validates customer exists, products exist, and creates order with items.
    
    Args:
        db: Database session
        customer_id: Customer ID
        items: List of dicts with keys: product_id, quantity, unit_price (optional)
    
    Returns:
        Created Order instance with items
        
    Raises:
        OrderValidationError: If validation fails
    """
    # Validate customer exists
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise OrderValidationError(f"Customer with ID {customer_id} not found")
    
    # Validate items
    if not items or len(items) == 0:
        raise OrderValidationError("Order must have at least one item")
    
    # Validate each product exists and prepare items
    validated_items = []
    for item in items:
        if "product_id" not in item:
            raise OrderValidationError("Each item must have a product_id")
        
        product_id = item["product_id"]
        product = get_product_by_id(db, product_id)
        if not product:
            raise OrderValidationError(f"Product with ID {product_id} not found")
        
        quantity = item.get("quantity", 1.0)
        if quantity <= 0:
            raise OrderValidationError(f"Quantity must be positive for product {product_id}")
        
        # Use provided unit_price or default to product price
        unit_price = item.get("unit_price", product.price)
        
        validated_items.append({
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price,
        })
    
    try:
        # Create order
        order_data = {
            "customer_id": customer_id,
            "status": OrderStatus.NEW,
            "order_date": datetime.now(),
        }
        order = create_order(db, order_data)
        
        # Create order items
        for item_data in validated_items:
            item_data["order_id"] = order.id
            create_order_item(db, item_data)
        
        # Refresh to get items relationship
        db.refresh(order)
        return order
        
    except IntegrityError as e:
        db.rollback()
        raise OrderValidationError(f"Failed to create order: {str(e)}")


def cancel_order(db: Session, order_id: int) -> Order:
    """
    Cancel an order if not yet delivered or in production.
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        Updated Order instance
        
    Raises:
        OrderNotFoundError: If order not found
        OrderCancellationError: If order cannot be cancelled
    """
    order = get_order_by_id(db, order_id)
    if not order:
        raise OrderNotFoundError(f"Order with ID {order_id} not found")
    
    # Check if order is already cancelled or completed
    if order.status == OrderStatus.CANCELLED:
        raise OrderCancellationError("Order is already cancelled")
    
    if order.status == OrderStatus.COMPLETED:
        raise OrderCancellationError("Cannot cancel completed order")
    
    # Check if any work orders are in progress
    for item in order.items:
        for work_order in item.work_orders:
            if work_order.status.value == "IN_PROGRESS":
                raise OrderCancellationError(
                    f"Cannot cancel order: Work order {work_order.id} is in progress"
                )
    
    # Check if any deliveries exist
    if order.deliveries and len(order.deliveries) > 0:
        raise OrderCancellationError("Cannot cancel order with deliveries")
    
    try:
        updated = update_order(db, order_id, {"status": OrderStatus.CANCELLED})
        if not updated:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        return updated
    except IntegrityError as e:
        db.rollback()
        raise OrderValidationError(f"Failed to cancel order: {str(e)}")


def get_order_status(db: Session, order_id: int) -> Dict[str, Any]:
    """
    Get consolidated order status across production, delivery, and invoice.
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        Dictionary with comprehensive order status
        
    Raises:
        OrderNotFoundError: If order not found
    """
    order = get_order_by_id(db, order_id)
    if not order:
        raise OrderNotFoundError(f"Order with ID {order_id} not found")
    
    # Collect work order statuses
    work_orders = []
    for item in order.items:
        for wo in item.work_orders:
            work_orders.append({
                "id": wo.id,
                "status": wo.status.value,
                "quantity": wo.quantity,
                "start_date": wo.start_date.isoformat() if wo.start_date else None,
                "end_date": wo.end_date.isoformat() if wo.end_date else None,
            })
    
    # Collect delivery statuses
    deliveries = []
    for delivery in order.deliveries:
        deliveries.append({
            "id": delivery.id,
            "status": delivery.status.value,
            "quantity": delivery.quantity,
            "delivered_at": delivery.delivered_at.isoformat() if delivery.delivered_at else None,
        })
    
    # Collect invoice statuses
    invoices = []
    for invoice in order.invoices:
        invoices.append({
            "id": invoice.id,
            "status": invoice.status.value,
            "total_amount": invoice.total_amount,
            "invoice_date": invoice.invoice_date.isoformat() if invoice.invoice_date else None,
        })
    
    return {
        "order_id": order.id,
        "status": order.status.value,
        "order_date": order.order_date.isoformat() if order.order_date else None,
        "delivery_date": order.delivery_date.isoformat() if order.delivery_date else None,
        "customer_id": order.customer_id,
        "items_count": len(order.items),
        "work_orders": work_orders,
        "deliveries": deliveries,
        "invoices": invoices,
    }


def list_orders_by_customer(db: Session, customer_id: int) -> List[Order]:
    """
    Fetch all orders for a given customer.
    
    Args:
        db: Database session
        customer_id: Customer ID
    
    Returns:
        List of Order instances
        
    Raises:
        OrderValidationError: If customer not found
    """
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise OrderValidationError(f"Customer with ID {customer_id} not found")
    
    return db.query(Order).filter(Order.customer_id == customer_id).all()


def get_order_by_id_service(db: Session, order_id: int) -> Order:
    """
    Get order by ID with error handling.
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        Order instance
        
    Raises:
        OrderNotFoundError: If order not found
    """
    order = get_order_by_id(db, order_id)
    if not order:
        raise OrderNotFoundError(f"Order with ID {order_id} not found")
    return order


def list_orders_service(db: Session, skip: int = 0, limit: int = 10) -> List[Order]:
    """
    List orders with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of Order instances
    """
    return list_orders(db, skip=skip, limit=limit)
