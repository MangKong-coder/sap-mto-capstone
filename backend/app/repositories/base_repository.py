"""Shared repository abstractions for SQLModel-based data access."""

from __future__ import annotations

from typing import Any, Iterable, Optional, Type, TypeVar, Generic

from sqlmodel import Session, SQLModel, select

from app.repositories.exceptions import EntityNotFoundError

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    """Base class providing common CRUD utilities for repositories."""

    def __init__(self, model: Type[T]) -> None:
        """Initialize the repository with a SQLModel type."""
        self.model = model

    def create(self, session: Session, obj_data: dict[str, Any]) -> T:
        """Persist a new model instance using the provided attribute mapping."""
        obj = self.model(**obj_data)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def get(self, session: Session, entity_id: int) -> Optional[T]:
        """Retrieve an entity by its identifier or return ``None`` when missing."""
        return session.get(self.model, entity_id)

    def get_or_raise(self, session: Session, entity_id: int) -> T:
        """Retrieve an entity or raise ``EntityNotFoundError`` if absent."""
        entity = self.get(session, entity_id)
        if entity is None:
            raise EntityNotFoundError(self.model.__name__, entity_id)
        return entity

    def list(
        self,
        session: Session,
        *,
        filters: Optional[Iterable[Any]] = None,
        offset: int = 0,
        limit: Optional[int] = None,
    ) -> list[T]:
        """Return a sequence of entities matching the optional filter set."""
        statement = select(self.model)
        if filters:
            for condition in filters:
                statement = statement.where(condition)
        if offset:
            statement = statement.offset(offset)
        if limit is not None:
            statement = statement.limit(limit)
        return session.exec(statement).all()

    def update(self, session: Session, entity_id: int, data: dict[str, Any]) -> T:
        """Apply partial updates to an entity and return the refreshed instance."""
        entity = self.get_or_raise(session, entity_id)
        for key, value in data.items():
            setattr(entity, key, value)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    def delete(self, session: Session, entity_id: int) -> bool:
        """Remove an entity and return ``True``; raise if the entity is missing."""
        entity = self.get_or_raise(session, entity_id)
        session.delete(entity)
        session.commit()
        return True
