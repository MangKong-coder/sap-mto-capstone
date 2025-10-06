"""Customer service providing customer-facing utilities."""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import func
from sqlmodel import Session

from app.models import Customer
from app.repositories.customer_repository import CustomerRepository

customer_repo = CustomerRepository()


def list_customers(
    session: Session,
    *,
    search: str | None = None,
) -> Sequence[Customer]:
    """Return customers optionally filtered by a case-insensitive search query."""

    filters = None
    if search:
        pattern = f"%{search.lower()}%"
        filters = [func.lower(Customer.name).like(pattern)]

    return customer_repo.list(session, filters=filters)
