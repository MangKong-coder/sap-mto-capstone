"""
Work Center API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.work_center import WorkCenterCreate, WorkCenterResponse
from app.crud.work_centers import (
    get_work_center,
    get_work_centers,
    create_work_center,
    update_work_center,
    delete_work_center,
)


router = APIRouter(prefix="/work-centers", tags=["Work Centers"])


@router.get("", response_model=List[WorkCenterResponse])
def list_work_centers(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db_session)
):
    """List all work centers with pagination."""
    skip = (page - 1) * size
    work_centers = get_work_centers(db, skip=skip, limit=size)
    return work_centers


@router.get("/{work_center_id}", response_model=WorkCenterResponse)
def get_work_center_endpoint(
    work_center_id: int,
    db: Session = Depends(get_db_session)
):
    """Get a work center by ID."""
    work_center = get_work_center(db, work_center_id=work_center_id)
    if work_center is None:
        raise HTTPException(status_code=404, detail="Work center not found")
    return work_center


@router.post("", response_model=WorkCenterResponse, status_code=201)
def create_work_center_endpoint(
    work_center: WorkCenterCreate,
    db: Session = Depends(get_db_session)
):
    """Create a new work center."""
    return create_work_center(db=db, work_center=work_center)


@router.put("/{work_center_id}", response_model=WorkCenterResponse)
def update_work_center_endpoint(
    work_center_id: int,
    work_center: WorkCenterCreate,
    db: Session = Depends(get_db_session)
):
    """Update an existing work center."""
    updated_work_center = update_work_center(db, work_center_id, work_center)
    if updated_work_center is None:
        raise HTTPException(status_code=404, detail="Work center not found")
    return updated_work_center


@router.delete("/{work_center_id}")
def delete_work_center_endpoint(
    work_center_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete a work center."""
    success = delete_work_center(db, work_center_id)
    if not success:
        raise HTTPException(status_code=404, detail="Work center not found")
    return {"message": "Work center deleted successfully"}
