"""
Component Usage API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.component_usage import (
    ComponentUsageCreate,
    ComponentUsageResponse,
    ComponentUsageSummaryResponse,
)
from app.services import (
    record_component_usage,
    get_usage_by_work_order,
    summarize_component_usage,
    get_component_usage_by_id_service,
    list_component_usages_service,
    get_component_usage_by_component,
    ComponentUsageValidationError,
    ComponentUsageNotFoundError,
)


router = APIRouter(prefix="/component-usage", tags=["Component Usage"])


@router.post("", response_model=ComponentUsageResponse, status_code=201)
def create_component_usage(
    usage: ComponentUsageCreate,
    db: Session = Depends(get_db_session)
):
    """Record component usage against work order."""
    try:
        result = record_component_usage(db, usage.model_dump())
        return result
    except ComponentUsageValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{usage_id}", response_model=ComponentUsageResponse)
def get_usage(
    usage_id: int,
    db: Session = Depends(get_db_session)
):
    """Get component usage by ID."""
    try:
        result = get_component_usage_by_id_service(db, usage_id)
        return result
    except ComponentUsageNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/work-order/{work_order_id}", response_model=List[ComponentUsageResponse])
def list_usage_by_work_order(
    work_order_id: int,
    db: Session = Depends(get_db_session)
):
    """List component usage by work order."""
    try:
        results = get_usage_by_work_order(db, work_order_id)
        return results
    except ComponentUsageNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/component/{component_id}", response_model=List[ComponentUsageResponse])
def list_usage_by_component(
    component_id: int,
    db: Session = Depends(get_db_session)
):
    """List component usage by component."""
    try:
        results = get_component_usage_by_component(db, component_id)
        return results
    except ComponentUsageNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/order/{order_id}/summary", response_model=List[ComponentUsageSummaryResponse])
def get_order_usage_summary(
    order_id: int,
    db: Session = Depends(get_db_session)
):
    """Summarize component usage for an order."""
    try:
        results = summarize_component_usage(db, order_id)
        return results
    except ComponentUsageNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[ComponentUsageResponse])
def list_component_usages(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List all component usages with pagination."""
    skip = (page - 1) * size
    results = list_component_usages_service(db, skip=skip, limit=size)
    return results
