"""Sales order repository implementation."""

from __future__ import annotations

from sqlmodel import Session, select

from app.models import SalesOrder, SalesOrderStatus
from app.repositories.base_repository import BaseRepository


class SalesOrderRepository(BaseRepository[SalesOrder]):
    """Data access helpers for ``SalesOrder`` entities."""

    def __init__(self) -> None:
        super().__init__(SalesOrder)

    def list_by_customer(self, session: Session, customer_id: int) -> list[SalesOrder]:
        """Return sales orders associated with the provided customer."""
        statement = select(SalesOrder).where(SalesOrder.customer_id == customer_id)
        return session.exec(statement).all()

    def list_by_status(self, session: Session, status: SalesOrderStatus) -> list[SalesOrder]:
        """Return sales orders filtered by status."""
        statement = select(SalesOrder).where(SalesOrder.status == status)
        return session.exec(statement).all()

    def update_status(self, session: Session, order_id: int, status: SalesOrderStatus) -> SalesOrder:
        """Update the status for a sales order and return the refreshed entity."""
        return self.update(session, order_id, {"status": status})
