"""Product service providing higher-level inventory operations."""

from __future__ import annotations

import logging
from typing import Any, Mapping, Sequence

from sqlalchemy import func
from sqlmodel import Session

from app.models import Product
from app.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

product_repo = ProductRepository()


def get_product_catalog(
    session: Session,
    *,
    search: str | None = None,
) -> Sequence[Product]:
    """Return all products optionally filtered by a case-insensitive search term."""

    filters = None
    if search:
        pattern = f"%{search.lower()}%"
        filters = [func.lower(Product.name).like(pattern)]

    return product_repo.list(session, filters=filters)


def create_product_with_stock(
    session: Session,
    product_data: Mapping[str, Any],
    stock_qty: int | None = None,
) -> Product:
    """Create a product and optionally seed its stock quantity."""

    payload = dict(product_data)
    if stock_qty is not None:
        if stock_qty < 0:
            raise ValueError("stock_qty cannot be negative")
        payload["stock_qty"] = stock_qty

    product = product_repo.create(session, payload)
    logger.info("Created product %s", product.id)
    return product


def get_product(session: Session, product_id: int) -> Product:
    """Retrieve a single product by ID."""
    return product_repo.get_or_raise(session, product_id)


def update_product(session: Session, product_id: int, product_data: Mapping[str, Any]) -> Product:
    """Update an existing product with new data."""
    product = product_repo.get_or_raise(session, product_id)
    updated = product_repo.update(session, product_id, product_data)
    logger.info("Updated product %s", product_id)
    return updated


def delete_product(session: Session, product_id: int) -> None:
    """Delete a product by ID."""
    product = product_repo.get_or_raise(session, product_id)
    product_repo.delete(session, product_id)
    logger.info("Deleted product %s", product_id)
