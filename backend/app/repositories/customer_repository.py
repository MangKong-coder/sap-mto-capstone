"""Customer repository implementation."""

from __future__ import annotations

from typing import Optional

from sqlmodel import Session, select

from app.models import Customer
from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """Data access functionality for ``Customer`` entities."""

    def __init__(self) -> None:
        super().__init__(Customer)

    def find_by_email(self, session: Session, email: str) -> Optional[Customer]:
        """Return a customer when the provided email address matches."""
        statement = select(Customer).where(Customer.email == email)
        return session.exec(statement).first()
