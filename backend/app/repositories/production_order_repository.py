"""Production order repository implementation."""

from __future__ import annotations

from sqlmodel import Session, select

from app.models import ProductionOrder, ProductionOrderStatus
from app.repositories.base_repository import BaseRepository


class ProductionOrderRepository(BaseRepository[ProductionOrder]):
    """Data access helpers for ``ProductionOrder`` entities."""

    def __init__(self) -> None:
        super().__init__(ProductionOrder)

    def list_by_status(self, session: Session, status: ProductionOrderStatus) -> list[ProductionOrder]:
        """Return production orders filtered by status."""
        statement = select(ProductionOrder).where(ProductionOrder.status == status)
        return session.exec(statement).all()

    def list_by_sales_order(self, session: Session, sales_order_id: int) -> list[ProductionOrder]:
        """Return production orders associated with a sales order."""
        statement = select(ProductionOrder).where(ProductionOrder.sales_order_id == sales_order_id)
        return session.exec(statement).all()
