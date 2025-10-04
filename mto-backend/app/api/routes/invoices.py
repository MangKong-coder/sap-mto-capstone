"""
Invoice API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceResponse,
)
from app.services import (
    generate_invoice,
    mark_invoice_paid,
    post_invoice,
    cancel_invoice,
    get_outstanding_invoices,
    get_invoice_by_id_service,
    list_invoices_service,
    list_invoices_by_order,
    InvoiceValidationError,
    InvoiceNotFoundError,
)


router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("", response_model=InvoiceResponse, status_code=201)
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db_session)
):
    """Generate a new invoice."""
    try:
        result = generate_invoice(db, invoice.model_dump())
        return result
    except InvoiceValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{invoice_id}/pay", response_model=InvoiceResponse)
def pay_invoice(
    invoice_id: int,
    db: Session = Depends(get_db_session)
):
    """Mark invoice as paid."""
    try:
        result = mark_invoice_paid(db, invoice_id)
        return result
    except InvoiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvoiceValidationError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{invoice_id}/post", response_model=InvoiceResponse)
def post_invoice_endpoint(
    invoice_id: int,
    db: Session = Depends(get_db_session)
):
    """Post invoice (DRAFT → POSTED)."""
    try:
        result = post_invoice(db, invoice_id)
        return result
    except InvoiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvoiceValidationError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{invoice_id}/cancel", response_model=InvoiceResponse)
def cancel_invoice_endpoint(
    invoice_id: int,
    db: Session = Depends(get_db_session)
):
    """Cancel an invoice."""
    try:
        result = cancel_invoice(db, invoice_id)
        return result
    except InvoiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvoiceValidationError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db_session)
):
    """Get invoice by ID."""
    try:
        result = get_invoice_by_id_service(db, invoice_id)
        return result
    except InvoiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/customer/{customer_id}/outstanding", response_model=List[InvoiceResponse])
def list_outstanding_invoices(
    customer_id: int,
    db: Session = Depends(get_db_session)
):
    """Get unpaid invoices for a customer."""
    try:
        results = get_outstanding_invoices(db, customer_id)
        return results
    except InvoiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/order/{order_id}", response_model=List[InvoiceResponse])
def list_order_invoices_endpoint(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """List invoices for an order."""
    try:
        results = list_invoices_by_order(db, order_id)
        return results
    except InvoiceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[InvoiceResponse])
def list_invoices(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List invoices with pagination."""
    skip = (page - 1) * size
    results = list_invoices_service(db, skip=skip, limit=size)
    return results
