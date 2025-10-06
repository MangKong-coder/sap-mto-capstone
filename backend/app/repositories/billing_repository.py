"""Billing repository implementation."""

from __future__ import annotations

from typing import Optional

from sqlmodel import Session, select

from app.models import Billing
from app.repositories.base_repository import BaseRepository


class BillingRepository(BaseRepository[Billing]):
    """Data access helpers for ``Billing`` entities."""

    def __init__(self) -> None:
        super().__init__(Billing)

    def get_by_sales_order(self, session: Session, sales_order_id: int) -> Optional[Billing]:
        """Return the billing record for the specified sales order."""
        statement = select(Billing).where(Billing.sales_order_id == sales_order_id)
        return session.exec(statement).first()
