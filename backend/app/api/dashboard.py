"""Dashboard API router implementation."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas.common import SuccessResponse
from app.schemas.dashboard import DashboardSummaryResponse
from app.services import dashboard_service

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=SuccessResponse[DashboardSummaryResponse])
def get_dashboard_summary(
    session: Session = Depends(get_session),
) -> SuccessResponse[DashboardSummaryResponse]:
    """Aggregate KPIs for admin dashboard."""

    try:
        summary = dashboard_service.get_dashboard_summary(session)
        return SuccessResponse(data=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
