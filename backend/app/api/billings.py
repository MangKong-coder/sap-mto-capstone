"""Billings API router implementation."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas.billings import BillingCreateRequest, BillingResponse
from app.schemas.common import SuccessResponse
from app.services import billing_service

router = APIRouter(prefix="/api/billings", tags=["Billings"], redirect_slashes=False)


@router.get("/", response_model=SuccessResponse[list[BillingResponse]])
def list_billings(
    session: Session = Depends(get_session),
) -> SuccessResponse[list[BillingResponse]]:
    """Retrieve all billing records."""

    try:
        billings = billing_service.list_billings(session)
        return SuccessResponse(data=billings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{billing_id}", response_model=SuccessResponse[BillingResponse])
def get_billing(
    billing_id: int,
    session: Session = Depends(get_session),
) -> SuccessResponse[BillingResponse]:
    """Retrieve specific billing record."""

    try:
        billing = billing_service.get_billing(session, billing_id)
        return SuccessResponse(data=billing)
    except billing_service.EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Billing not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=SuccessResponse[BillingResponse])
def generate_billing(
    request: BillingCreateRequest,
    session: Session = Depends(get_session),
) -> SuccessResponse[BillingResponse]:
    """Generate a billing record after delivery."""

    try:
        billing = billing_service.generate_billing_for_order(
            session,
            request.sales_order_id,
        )
        return SuccessResponse(data=billing)
    except billing_service.InvalidTransitionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
