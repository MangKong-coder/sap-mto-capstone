"""Delivery repository implementation."""

from __future__ import annotations

from sqlmodel import Session, select

from app.models import Delivery, DeliveryStatus
from app.repositories.base_repository import BaseRepository


class DeliveryRepository(BaseRepository[Delivery]):
    """Data access helpers for ``Delivery`` entities."""

    def __init__(self) -> None:
        super().__init__(Delivery)

    def list_by_status(self, session: Session, status: DeliveryStatus) -> list[Delivery]:
        """Return deliveries filtered by their status."""
        statement = select(Delivery).where(Delivery.status == status)
        return session.exec(statement).all()

    def list_by_sales_order(self, session: Session, sales_order_id: int) -> list[Delivery]:
        """Return deliveries associated with a specific sales order."""
        statement = select(Delivery).where(Delivery.sales_order_id == sales_order_id)
        return session.exec(statement).all()
