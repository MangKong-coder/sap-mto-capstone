"""
Customer Service - Business logic for customer management.
Handles customer lifecycle with validation and business rules.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.repositories import (
    create_customer,
    get_customer_by_id,
    list_customers,
    update_customer,
)
from app.models import Customer, Order


class CustomerServiceError(Exception):
    """Base exception for customer service errors."""
    pass


class CustomerValidationError(CustomerServiceError):
    """Raised when customer validation fails."""
    pass


class CustomerNotFoundError(CustomerServiceError):
    """Raised when customer is not found."""
    pass


def register_customer(db: Session, data: dict) -> Customer:
    """
    Register a new customer with validation.
    
    Validates required fields and ensures email uniqueness.
    
    Args:
        db: Database session
        data: Dictionary with customer data (name, email, phone, address)
    
    Returns:
        Created Customer instance
        
    Raises:
        CustomerValidationError: If validation fails
    """
    # Validate required fields
    if not data.get("name"):
        raise CustomerValidationError("Customer name is required")
    
    # Validate email format if provided
    email = data.get("email")
    if email and "@" not in email:
        raise CustomerValidationError("Invalid email format")
    
    # Check email uniqueness if provided
    if email:
        existing = db.query(Customer).filter(Customer.email == email).first()
        if existing:
            raise CustomerValidationError(f"Customer with email {email} already exists")
    
    try:
        return create_customer(db, data)
    except IntegrityError as e:
        db.rollback()
        raise CustomerValidationError(f"Failed to create customer: {str(e)}")


def update_customer_profile(db: Session, customer_id: int, data: dict) -> Customer:
    """
    Update customer profile with validation.
    
    Enforces uniqueness constraints and prevents invalid changes.
    
    Args:
        db: Database session
        customer_id: Customer ID
        data: Dictionary with fields to update
    
    Returns:
        Updated Customer instance
        
    Raises:
        CustomerNotFoundError: If customer not found
        CustomerValidationError: If validation fails
    """
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")
    
    # Validate email format if being updated
    if "email" in data:
        email = data["email"]
        if email and "@" not in email:
            raise CustomerValidationError("Invalid email format")
        
        # Check email uniqueness
        if email:
            existing = db.query(Customer).filter(
                Customer.email == email,
                Customer.id != customer_id
            ).first()
            if existing:
                raise CustomerValidationError(f"Email {email} already in use")
    
    # Prevent empty name
    if "name" in data and not data["name"]:
        raise CustomerValidationError("Customer name cannot be empty")
    
    try:
        updated = update_customer(db, customer_id, data)
        if not updated:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")
        return updated
    except IntegrityError as e:
        db.rollback()
        raise CustomerValidationError(f"Failed to update customer: {str(e)}")


def get_customer_orders(db: Session, customer_id: int) -> List[Order]:
    """
    Retrieve all orders linked to a customer.
    
    Args:
        db: Database session
        customer_id: Customer ID
    
    Returns:
        List of Order instances
        
    Raises:
        CustomerNotFoundError: If customer not found
    """
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")
    
    return customer.orders


def get_customer_by_id_service(db: Session, customer_id: int) -> Customer:
    """
    Get customer by ID with error handling.
    
    Args:
        db: Database session
        customer_id: Customer ID
    
    Returns:
        Customer instance
        
    Raises:
        CustomerNotFoundError: If customer not found
    """
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")
    return customer


def list_customers_service(db: Session, skip: int = 0, limit: int = 10) -> List[Customer]:
    """
    List customers with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of Customer instances
    """
    return list_customers(db, skip=skip, limit=limit)
