"""
Work Center CRUD operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import WorkCenter
from app.schemas.work_center import WorkCenterCreate


def get_work_center(db: Session, work_center_id: int) -> Optional[WorkCenter]:
    """Get a work center by ID."""
    return db.query(WorkCenter).filter(WorkCenter.id == work_center_id).first()


def get_work_centers(db: Session, skip: int = 0, limit: int = 100) -> List[WorkCenter]:
    """Get all work centers with pagination."""
    return db.query(WorkCenter).offset(skip).limit(limit).all()


def create_work_center(db: Session, work_center: WorkCenterCreate) -> WorkCenter:
    """Create a new work center."""
    db_work_center = WorkCenter(**work_center.dict())
    db.add(db_work_center)
    db.commit()
    db.refresh(db_work_center)
    return db_work_center


def update_work_center(db: Session, work_center_id: int, work_center: WorkCenterCreate) -> Optional[WorkCenter]:
    """Update an existing work center."""
    db_work_center = db.query(WorkCenter).filter(WorkCenter.id == work_center_id).first()
    if db_work_center:
        for key, value in work_center.dict().items():
            setattr(db_work_center, key, value)
        db.commit()
        db.refresh(db_work_center)
    return db_work_center


def delete_work_center(db: Session, work_center_id: int) -> bool:
    """Delete a work center."""
    db_work_center = db.query(WorkCenter).filter(WorkCenter.id == work_center_id).first()
    if db_work_center:
        db.delete(db_work_center)
        db.commit()
        return True
    return False
