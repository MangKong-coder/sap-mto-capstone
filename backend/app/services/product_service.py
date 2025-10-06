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
    logger.info("Created product %s with stock %s", product.id, product.stock_qty)
    return product


def restock_product(session: Session, product_id: int, quantity: int) -> Product:
    """Increase the stock level for a product by the specified quantity."""

    if quantity <= 0:
        raise ValueError("quantity must be greater than zero")

    product = product_repo.get_or_raise(session, product_id)
    current_stock = product.stock_qty or 0
    new_stock = current_stock + quantity

    updated = product_repo.update(session, product_id, {"stock_qty": new_stock})
    logger.info(
        "Product %s restocked from %s to %s",
        product_id,
        current_stock,
        new_stock,
    )
    return updated
