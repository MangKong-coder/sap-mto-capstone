"""
Repository layer for Customer entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Customer


def create_customer(db: Session, data: dict) -> Customer:
    """
    Create a new customer.

    Args:
        db: Database session
        data: Dictionary containing customer data (name, email, phone, address)

    Returns:
        Created Customer instance
    """
    db_customer = Customer(**data)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customer_by_id(db: Session, customer_id: int) -> Optional[Customer]:
    """
    Retrieve a customer by ID.

    Args:
        db: Database session
        customer_id: Customer ID

    Returns:
        Customer instance if found, None otherwise
    """
    return db.query(Customer).filter(Customer.id == customer_id).first()


def list_customers(db: Session, skip: int = 0, limit: int = 10) -> List[Customer]:
    """
    List customers with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Customer instances
    """
    return db.query(Customer).offset(skip).limit(limit).all()


def update_customer(db: Session, customer_id: int, data: dict) -> Optional[Customer]:
    """
    Update a customer by ID.

    Args:
        db: Database session
        customer_id: Customer ID
        data: Dictionary containing fields to update

    Returns:
        Updated Customer instance if found, None otherwise
    """
    db_customer = get_customer_by_id(db, customer_id)
    if not db_customer:
        return None

    for key, value in data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int) -> bool:
    """
    Delete a customer by ID.

    Args:
        db: Database session
        customer_id: Customer ID

    Returns:
        True if deleted, False if not found
    """
    db_customer = get_customer_by_id(db, customer_id)
    if not db_customer:
        return False

    db.delete(db_customer)
    db.commit()
    return True
