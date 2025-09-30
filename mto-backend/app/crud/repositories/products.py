"""
Repository layer for Product entity.
Provides primitive CRUD operations for database access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Product


def create_product(db: Session, data: dict) -> Product:
    """
    Create a new product.

    Args:
        db: Database session
        data: Dictionary containing product data (sku, name, description, price)

    Returns:
        Created Product instance
    """
    db_product = Product(**data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    """
    Retrieve a product by ID.

    Args:
        db: Database session
        product_id: Product ID

    Returns:
        Product instance if found, None otherwise
    """
    return db.query(Product).filter(Product.id == product_id).first()


def list_products(db: Session, skip: int = 0, limit: int = 10) -> List[Product]:
    """
    List products with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Product instances
    """
    return db.query(Product).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, data: dict) -> Optional[Product]:
    """
    Update a product by ID.

    Args:
        db: Database session
        product_id: Product ID
        data: Dictionary containing fields to update

    Returns:
        Updated Product instance if found, None otherwise
    """
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None

    for key, value in data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """
    Delete a product by ID.

    Args:
        db: Database session
        product_id: Product ID

    Returns:
        True if deleted, False if not found
    """
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True
