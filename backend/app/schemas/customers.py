"""Pydantic schemas for customer API endpoints."""

from __future__ import annotations

from pydantic import BaseModel


class CustomerResponse(BaseModel):
    """Response payload describing a customer."""

    id: int
    name: str
    email: str
    role: str
