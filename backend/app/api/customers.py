"""Customers API router implementation."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas.common import SuccessResponse
from app.schemas.customers import CustomerResponse
from app.services import customer_service

router = APIRouter(prefix="/api/customers", tags=["Customers"], redirect_slashes=False)


@router.get("/", response_model=SuccessResponse[list[CustomerResponse]])
def list_customers(
    search: str | None = Query(default=None, description="Search customers by name"),
    session: Session = Depends(get_session),
) -> SuccessResponse[list[CustomerResponse]]:
    """List all customers, with optional search."""

    try:
        customers = customer_service.list_customers(session, search=search)
        return SuccessResponse(data=customers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
