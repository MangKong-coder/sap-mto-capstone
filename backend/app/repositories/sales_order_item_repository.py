"""Sales order item repository implementation."""

from __future__ import annotations

from sqlmodel import Session, select

from app.models import SalesOrderItem
from app.repositories.base_repository import BaseRepository


class SalesOrderItemRepository(BaseRepository[SalesOrderItem]):
    """Data access helpers for ``SalesOrderItem`` entities."""

    def __init__(self) -> None:
        super().__init__(SalesOrderItem)

    def list_by_order(self, session: Session, order_id: int) -> list[SalesOrderItem]:
        """Return items belonging to the specified sales order."""
        statement = select(SalesOrderItem).where(SalesOrderItem.sales_order_id == order_id)
        return session.exec(statement).all()
