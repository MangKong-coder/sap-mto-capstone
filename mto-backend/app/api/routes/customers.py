"""
Customer API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)
from app.schemas.order import OrderResponse
from app.services import (
    register_customer,
    update_customer_profile,
    get_customer_orders,
    get_customer_by_id_service,
    list_customers_service,
    CustomerValidationError,
    CustomerNotFoundError,
)


router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=CustomerResponse, status_code=201)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db_session)
):
    """Register a new customer."""
    try:
        result = register_customer(db, customer.model_dump())
        return result
    except CustomerValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db_session)
):
    """Update customer profile."""
    try:
        result = update_customer_profile(
            db, customer_id, customer.model_dump(exclude_unset=True)
        )
        return result
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CustomerValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db_session)
):
    """Get customer by ID."""
    try:
        result = get_customer_by_id_service(db, customer_id)
        return result
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{customer_id}/orders", response_model=List[OrderResponse])
def get_customer_order_list(
    customer_id: int,
    db: Session = Depends(get_db_session)
):
    """Get orders for a customer."""
    try:
        results = get_customer_orders(db, customer_id)
        return results
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[CustomerResponse])
def list_customers(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List customers with pagination."""
    skip = (page - 1) * size
    results = list_customers_service(db, skip=skip, limit=size)
    return results
