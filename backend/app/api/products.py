"""Products API router implementation."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas.common import SuccessResponse
from app.schemas.products import ProductCreateRequest, ProductResponse
from app.services import product_service

router = APIRouter(prefix="/api/products", tags=["Products"])


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
            request.stock_qty,
        )
        return SuccessResponse(data=product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
