"""Shared Pydantic schema components for API responses."""

from __future__ import annotations

from typing import Generic, Literal, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Base schema for successful API responses including the data payload."""

    success: Literal[True] = True
    data: T
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Schema for standardized error responses."""

    success: Literal[False] = False
    error: str
    message: str
