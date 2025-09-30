"""
Repository layer for Invoice entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Invoice


def create_invoice(db: Session, data: dict) -> Invoice:
    """
    Create a new invoice.

    Args:
        db: Database session
        data: Dictionary containing invoice data (order_id, invoice_date, status, total_amount)

    Returns:
        Created Invoice instance
    """
    db_invoice = Invoice(**data)
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def get_invoice_by_id(db: Session, invoice_id: int) -> Optional[Invoice]:
    """
    Retrieve an invoice by ID.

    Args:
        db: Database session
        invoice_id: Invoice ID

    Returns:
        Invoice instance if found, None otherwise
    """
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()


def list_invoices(db: Session, skip: int = 0, limit: int = 10) -> List[Invoice]:
    """
    List invoices with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Invoice instances
    """
    return db.query(Invoice).offset(skip).limit(limit).all()


def update_invoice(db: Session, invoice_id: int, data: dict) -> Optional[Invoice]:
    """
    Update an invoice by ID.

    Args:
        db: Database session
        invoice_id: Invoice ID
        data: Dictionary containing fields to update

    Returns:
        Updated Invoice instance if found, None otherwise
    """
    db_invoice = get_invoice_by_id(db, invoice_id)
    if not db_invoice:
        return None

    for key, value in data.items():
        setattr(db_invoice, key, value)

    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def delete_invoice(db: Session, invoice_id: int) -> bool:
    """
    Delete an invoice by ID.

    Args:
        db: Database session
        invoice_id: Invoice ID

    Returns:
        True if deleted, False if not found
    """
    db_invoice = get_invoice_by_id(db, invoice_id)
    if not db_invoice:
        return False

    db.delete(db_invoice)
    db.commit()
    return True
