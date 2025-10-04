"""
Component API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.component import (
    ComponentCreate,
    ComponentUpdate,
    ComponentResponse,
    ComponentAvailabilityResponse,
)
from app.services import (
    add_component,
    update_component_details,
    get_component_availability,
    get_component_by_part_code,
    get_component_by_id_service,
    list_components_service,
    ComponentValidationError,
    ComponentNotFoundError,
)


router = APIRouter(prefix="/components", tags=["Components"])


@router.post("", response_model=ComponentResponse, status_code=201)
def create_component(
    component: ComponentCreate,
    db: Session = Depends(get_db_session)
):
    """Add a new component."""
    try:
        result = add_component(db, component.model_dump())
        return result
    except ComponentValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{component_id}", response_model=ComponentResponse)
def update_component(
    component_id: int,
    component: ComponentUpdate,
    db: Session = Depends(get_db_session)
):
    """Update component details."""
    try:
        result = update_component_details(
            db, component_id, component.model_dump(exclude_unset=True)
        )
        return result
    except ComponentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ComponentValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{component_id}", response_model=ComponentResponse)
def get_component(
    component_id: int,
    db: Session = Depends(get_db_session)
):
    """Get component by ID."""
    try:
        result = get_component_by_id_service(db, component_id)
        return result
    except ComponentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/code/{part_code}", response_model=ComponentResponse)
def get_component_by_code(
    part_code: str,
    db: Session = Depends(get_db_session)
):
    """Get component by part code."""
    result = get_component_by_part_code(db, part_code)
    if not result:
        raise HTTPException(status_code=404, detail=f"Component with part code {part_code} not found")
    return result


@router.get("/{component_id}/availability", response_model=ComponentAvailabilityResponse)
def check_component_availability(
    component_id: int,
    db: Session = Depends(get_db_session)
):
    """Check component availability."""
    try:
        result = get_component_availability(db, component_id)
        return result
    except ComponentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[ComponentResponse])
def list_components(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List components with pagination."""
    skip = (page - 1) * size
    results = list_components_service(db, skip=skip, limit=size)
    return results
