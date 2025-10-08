"""Service layer specific exception classes."""

from __future__ import annotations


class ServiceError(Exception):
    """Base class for service-layer exceptions."""


class InvalidTransitionError(ServiceError):
    """Raised when a domain entity attempts an invalid status transition."""

    def __init__(self, entity_name: str, current_status: str, target_status: str) -> None:
        message = (
            f"Invalid status transition for {entity_name}: "
            f"{current_status!r} → {target_status!r}."
        )
        super().__init__(message)
        self.entity_name = entity_name
        self.current_status = current_status
        self.target_status = target_status


class EmailDeliveryError(ServiceError):
    """Raised when an outbound email fails to send."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
