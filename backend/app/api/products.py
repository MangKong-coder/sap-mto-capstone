"""Products API router implementation."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas.common import SuccessResponse
from app.schemas.products import ProductCreateRequest, ProductResponse, ProductUpdateRequest
from app.services import product_service

router = APIRouter(prefix="/api/products", tags=["Products"], redirect_slashes=False)


@router.get("/", response_model=SuccessResponse[list[ProductResponse]])
def list_products(
    search: str | None = Query(default=None, description="Search products by name"),
    session: Session = Depends(get_session),
) -> SuccessResponse[list[ProductResponse]]:
    """Retrieve full product catalog, optionally filtered by keyword."""

    try:
        products = product_service.get_product_catalog(session, search=search)
        return SuccessResponse(data=products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=SuccessResponse[ProductResponse])
def create_product(
    request: ProductCreateRequest,
    session: Session = Depends(get_session),
) -> SuccessResponse[ProductResponse]:
    """Add a new product."""

    try:
        product = product_service.create_product_with_stock(
            session,
            request.model_dump(),
        )
        return SuccessResponse(data=product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{product_id}", response_model=SuccessResponse[ProductResponse])
def get_product(
    product_id: int,
    session: Session = Depends(get_session),
) -> SuccessResponse[ProductResponse]:
    """Retrieve a single product by ID."""

    try:
        product = product_service.get_product(session, product_id)
        return SuccessResponse(data=product)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{product_id}", response_model=SuccessResponse[ProductResponse])
def update_product(
    product_id: int,
    request: ProductUpdateRequest,
    session: Session = Depends(get_session),
) -> SuccessResponse[ProductResponse]:
    """Update an existing product."""

    try:
        product = product_service.update_product(session, product_id, request.model_dump())
        return SuccessResponse(data=product)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
) -> SuccessResponse[None]:
    """Delete a product by ID."""

    try:
        product_service.delete_product(session, product_id)
        return SuccessResponse(data=None)
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        raise HTTPException(status_code=500, detail=str(e))
