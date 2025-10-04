"""
Product API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductAvailabilityResponse,
)
from app.services import (
    add_new_product,
    update_product_details,
    get_product_availability,
    get_product_by_sku,
    get_product_by_id_service,
    list_products_service,
    ProductValidationError,
    ProductNotFoundError,
)


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db_session)
):
    """Add a new product."""
    try:
        result = add_new_product(db, product.model_dump())
        return result
    except ProductValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db_session)
):
    """Update product details."""
    try:
        result = update_product_details(
            db, product_id, product.model_dump(exclude_unset=True)
        )
        return result
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProductValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db_session)
):
    """Get product by ID."""
    try:
        result = get_product_by_id_service(db, product_id)
        return result
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/sku/{sku}", response_model=ProductResponse)
def get_product_by_sku_endpoint(
    sku: str,
    db: Session = Depends(get_db_session)
):
    """Get product by SKU."""
    result = get_product_by_sku(db, sku)
    if not result:
        raise HTTPException(status_code=404, detail=f"Product with SKU {sku} not found")
    return result


@router.get("/{product_id}/availability", response_model=ProductAvailabilityResponse)
def check_product_availability(
    product_id: int,
    db: Session = Depends(get_db_session)
):
    """Check product availability."""
    try:
        result = get_product_availability(db, product_id)
        return result
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[ProductResponse])
def list_products(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List products with pagination."""
    skip = (page - 1) * size
    results = list_products_service(db, skip=skip, limit=size)
    return results
