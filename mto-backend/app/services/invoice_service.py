"""
Invoice Service - Business logic for billing and payment tracking.
Handles invoice generation and payment confirmation.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.repositories import (
    create_invoice,
    get_invoice_by_id,
    list_invoices,
    update_invoice,
    get_order_by_id,
)
from app.models import Invoice, InvoiceStatus, DeliveryStatus


class InvoiceServiceError(Exception):
    """Base exception for invoice service errors."""
    pass


class InvoiceValidationError(InvoiceServiceError):
    """Raised when invoice validation fails."""
    pass


class InvoiceNotFoundError(InvoiceServiceError):
    """Raised when invoice is not found."""
    pass


def generate_invoice(db: Session, order_id: int) -> Invoice:
    """
    Generate an invoice after delivery.
    
    Calculates total amount from order items and validates delivery exists.
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        Created Invoice instance
        
    Raises:
        InvoiceValidationError: If validation fails
    """
    # Validate order exists
    order = get_order_by_id(db, order_id)
    if not order:
        raise InvoiceValidationError(f"Order with ID {order_id} not found")
    
    # Check if deliveries exist
    if not order.deliveries or len(order.deliveries) == 0:
        raise InvoiceValidationError("Cannot generate invoice: No deliveries found for this order")
    
    # Check if at least one delivery is shipped or delivered
    has_valid_delivery = any(
        delivery.status in [DeliveryStatus.SHIPPED, DeliveryStatus.DELIVERED]
        for delivery in order.deliveries
    )
    
    if not has_valid_delivery:
        raise InvoiceValidationError(
            "Cannot generate invoice: No shipped or delivered items found"
        )
    
    # Calculate total amount from order items
    total_amount = 0.0
    for item in order.items:
        total_amount += item.quantity * item.unit_price
    
    if total_amount <= 0:
        raise InvoiceValidationError("Invoice total amount must be positive")
    
    # Check if invoice already exists
    existing_invoices = db.query(Invoice).filter(
        Invoice.order_id == order_id,
        Invoice.status != InvoiceStatus.CANCELLED
    ).all()
    
    if existing_invoices:
        raise InvoiceValidationError(
            f"Invoice already exists for order {order_id}"
        )
    
    try:
        data = {
            "order_id": order_id,
            "total_amount": total_amount,
            "invoice_date": datetime.now(),
            "status": InvoiceStatus.DRAFT,
        }
        return create_invoice(db, data)
    except IntegrityError as e:
        db.rollback()
        raise InvoiceValidationError(f"Failed to generate invoice: {str(e)}")


def mark_invoice_paid(db: Session, invoice_id: int, payment_date: Optional[datetime] = None) -> Invoice:
    """
    Mark an invoice as paid to confirm payment.
    
    Args:
        db: Database session
        invoice_id: Invoice ID
        payment_date: Optional payment timestamp (defaults to now)
    
    Returns:
        Updated Invoice instance
        
    Raises:
        InvoiceNotFoundError: If invoice not found
        InvoiceValidationError: If validation fails
    """
    invoice = get_invoice_by_id(db, invoice_id)
    if not invoice:
        raise InvoiceNotFoundError(f"Invoice with ID {invoice_id} not found")
    
    # Validate status
    if invoice.status == InvoiceStatus.PAID:
        raise InvoiceValidationError("Invoice is already marked as paid")
    
    if invoice.status == InvoiceStatus.CANCELLED:
        raise InvoiceValidationError("Cannot mark cancelled invoice as paid")
    
    # Post invoice first if it's still in draft
    if invoice.status == InvoiceStatus.DRAFT:
        invoice = post_invoice(db, invoice_id)
    
    try:
        update_data = {
            "status": InvoiceStatus.PAID,
            "invoice_date": payment_date or datetime.now(),
        }
        updated = update_invoice(db, invoice_id, update_data)
        if not updated:
            raise InvoiceNotFoundError(f"Invoice with ID {invoice_id} not found")
        return updated
    except IntegrityError as e:
        db.rollback()
        raise InvoiceValidationError(f"Failed to mark invoice as paid: {str(e)}")


def post_invoice(db: Session, invoice_id: int) -> Invoice:
    """
    Post an invoice (change from DRAFT to POSTED).
    
    Args:
        db: Database session
        invoice_id: Invoice ID
    
    Returns:
        Updated Invoice instance
        
    Raises:
        InvoiceNotFoundError: If invoice not found
        InvoiceValidationError: If validation fails
    """
    invoice = get_invoice_by_id(db, invoice_id)
    if not invoice:
        raise InvoiceNotFoundError(f"Invoice with ID {invoice_id} not found")
    
    if invoice.status != InvoiceStatus.DRAFT:
        raise InvoiceValidationError("Can only post draft invoices")
    
    try:
        updated = update_invoice(db, invoice_id, {"status": InvoiceStatus.POSTED})
        if not updated:
            raise InvoiceNotFoundError(f"Invoice with ID {invoice_id} not found")
        return updated
    except IntegrityError as e:
        db.rollback()
        raise InvoiceValidationError(f"Failed to post invoice: {str(e)}")


def cancel_invoice(db: Session, invoice_id: int) -> Invoice:
    """
    Cancel an invoice.
    
    Args:
        db: Database session
        invoice_id: Invoice ID
    
    Returns:
        Updated Invoice instance
        
    Raises:
        InvoiceNotFoundError: If invoice not found
        InvoiceValidationError: If validation fails
    """
    invoice = get_invoice_by_id(db, invoice_id)
    if not invoice:
        raise InvoiceNotFoundError(f"Invoice with ID {invoice_id} not found")
    
    if invoice.status == InvoiceStatus.PAID:
        raise InvoiceValidationError("Cannot cancel paid invoice")
    
    if invoice.status == InvoiceStatus.CANCELLED:
        raise InvoiceValidationError("Invoice is already cancelled")
    
    try:
        updated = update_invoice(db, invoice_id, {"status": InvoiceStatus.CANCELLED})
        if not updated:
            raise InvoiceNotFoundError(f"Invoice with ID {invoice_id} not found")
        return updated
    except IntegrityError as e:
        db.rollback()
        raise InvoiceValidationError(f"Failed to cancel invoice: {str(e)}")


def get_outstanding_invoices(db: Session, customer_id: int) -> List[Invoice]:
    """
    Track unpaid invoices for a customer.
    
    Args:
        db: Database session
        customer_id: Customer ID
    
    Returns:
        List of outstanding Invoice instances
    """
    from app.models import Order
    
    # Get all orders for this customer
    orders = db.query(Order).filter(Order.customer_id == customer_id).all()
    
    # Collect unpaid invoices
    outstanding = []
    for order in orders:
        for invoice in order.invoices:
            if invoice.status in [InvoiceStatus.DRAFT, InvoiceStatus.POSTED]:
                outstanding.append(invoice)
    
    return outstanding


def get_invoice_by_id_service(db: Session, invoice_id: int) -> Invoice:
    """
    Get invoice by ID with error handling.
    
    Args:
        db: Database session
        invoice_id: Invoice ID
    
    Returns:
        Invoice instance
        
    Raises:
        InvoiceNotFoundError: If invoice not found
    """
    invoice = get_invoice_by_id(db, invoice_id)
    if not invoice:
        raise InvoiceNotFoundError(f"Invoice with ID {invoice_id} not found")
    return invoice


def list_invoices_service(db: Session, skip: int = 0, limit: int = 10) -> List[Invoice]:
    """
    List invoices with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of Invoice instances
    """
    return list_invoices(db, skip=skip, limit=limit)


def list_invoices_by_order(db: Session, order_id: int) -> List[Invoice]:
    """
    List all invoices for a specific order.
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        List of Invoice instances
        
    Raises:
        InvoiceValidationError: If order not found
    """
    order = get_order_by_id(db, order_id)
    if not order:
        raise InvoiceValidationError(f"Order with ID {order_id} not found")
    
    return order.invoices
