"""Custom exceptions for repository operations."""

from dataclasses import dataclass


@dataclass
class EntityNotFoundError(Exception):
    """Exception raised when a requested entity cannot be located."""

    entity_name: str
    entity_id: int

    def __post_init__(self) -> None:
        message = f"{self.entity_name} with id={self.entity_id} not found."
        super().__init__(message)
