"""
Product Service - Business logic for product catalog management.
Handles product lifecycle with validation and stock tracking.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.repositories import (
    create_product,
    get_product_by_id,
    list_products,
    update_product,
)
from app.models import Product


class ProductServiceError(Exception):
    """Base exception for product service errors."""
    pass


class ProductValidationError(ProductServiceError):
    """Raised when product validation fails."""
    pass


class ProductNotFoundError(ProductServiceError):
    """Raised when product is not found."""
    pass


def add_new_product(db: Session, data: dict) -> Product:
    """
    Add a new product with SKU uniqueness validation.
    
    Args:
        db: Database session
        data: Dictionary with product data (sku, name, description, price)
    
    Returns:
        Created Product instance
        
    Raises:
        ProductValidationError: If validation fails
    """
    # Validate required fields
    if not data.get("sku"):
        raise ProductValidationError("Product SKU is required")
    if not data.get("name"):
        raise ProductValidationError("Product name is required")
    
    # Validate price
    price = data.get("price", 0.0)
    if price < 0:
        raise ProductValidationError("Price cannot be negative")
    
    # Check SKU uniqueness
    sku = data["sku"]
    existing = db.query(Product).filter(Product.sku == sku).first()
    if existing:
        raise ProductValidationError(f"Product with SKU {sku} already exists")
    
    try:
        return create_product(db, data)
    except IntegrityError as e:
        db.rollback()
        raise ProductValidationError(f"Failed to create product: {str(e)}")


def update_product_details(db: Session, product_id: int, data: dict) -> Product:
    """
    Update product details with validation.
    
    Note: In the current schema, products don't have stock fields.
    Stock is managed through production (work orders) and consumption.
    
    Args:
        db: Database session
        product_id: Product ID
        data: Dictionary with fields to update
    
    Returns:
        Updated Product instance
        
    Raises:
        ProductNotFoundError: If product not found
        ProductValidationError: If validation fails
    """
    product = get_product_by_id(db, product_id)
    if not product:
        raise ProductNotFoundError(f"Product with ID {product_id} not found")
    
    # Validate SKU uniqueness if being updated
    if "sku" in data:
        sku = data["sku"]
        if not sku:
            raise ProductValidationError("Product SKU cannot be empty")
        
        existing = db.query(Product).filter(
            Product.sku == sku,
            Product.id != product_id
        ).first()
        if existing:
            raise ProductValidationError(f"SKU {sku} already in use")
    
    # Validate name
    if "name" in data and not data["name"]:
        raise ProductValidationError("Product name cannot be empty")
    
    # Validate price
    if "price" in data and data["price"] < 0:
        raise ProductValidationError("Price cannot be negative")
    
    try:
        updated = update_product(db, product_id, data)
        if not updated:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        return updated
    except IntegrityError as e:
        db.rollback()
        raise ProductValidationError(f"Failed to update product: {str(e)}")


def get_product_availability(db: Session, product_id: int) -> dict:
    """
    Check product availability.
    
    Note: In the current MTO (Make-to-Order) schema, products don't have
    a stock field. Products are manufactured on demand. This function
    returns the product details and confirms it exists in the catalog.
    
    For actual inventory tracking, you would need to:
    1. Add a stock field to the Product model, or
    2. Track finished goods inventory in a separate table
    
    Args:
        db: Database session
        product_id: Product ID
    
    Returns:
        Dictionary with availability information
        
    Raises:
        ProductNotFoundError: If product not found
    """
    product = get_product_by_id(db, product_id)
    if not product:
        raise ProductNotFoundError(f"Product with ID {product_id} not found")
    
    return {
        "product_id": product.id,
        "sku": product.sku,
        "name": product.name,
        "price": product.price,
        "available": True,  # MTO products are always "available" to order
        "note": "This is a make-to-order product"
    }


def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
    """
    Get product by SKU.
    
    Args:
        db: Database session
        sku: Product SKU
    
    Returns:
        Product instance if found, None otherwise
    """
    return db.query(Product).filter(Product.sku == sku).first()


def get_product_by_id_service(db: Session, product_id: int) -> Product:
    """
    Get product by ID with error handling.
    
    Args:
        db: Database session
        product_id: Product ID
    
    Returns:
        Product instance
        
    Raises:
        ProductNotFoundError: If product not found
    """
    product = get_product_by_id(db, product_id)
    if not product:
        raise ProductNotFoundError(f"Product with ID {product_id} not found")
    return product


def list_products_service(db: Session, skip: int = 0, limit: int = 10) -> List[Product]:
    """
    List products with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of Product instances
    """
    return list_products(db, skip=skip, limit=limit)
