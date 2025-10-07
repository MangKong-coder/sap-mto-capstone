"""Product repository with convenience query helpers."""

from __future__ import annotations

from typing import Optional

from sqlmodel import Session, select

from app.models import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Data access helpers for ``Product`` entities."""

    def __init__(self) -> None:
        super().__init__(Product)

    def find_by_name(self, session: Session, name: str) -> Optional[Product]:
        """Return the first product matching the provided name."""
        statement = select(Product).where(Product.name == name)
        return session.exec(statement).first()
