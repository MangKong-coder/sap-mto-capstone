"""Production order service encapsulating manufacturing workflows."""

from __future__ import annotations

import logging
from datetime import datetime

from sqlmodel import Session

from app.models import (
    ProductionOrder,
    ProductionOrderStatus,
    SalesOrderStatus,
    current_utc_time,
)
from app.repositories.production_order_repository import ProductionOrderRepository
from app.repositories.sales_order_repository import SalesOrderRepository
from app.services.exceptions import InvalidTransitionError

logger = logging.getLogger(__name__)

production_repo = ProductionOrderRepository()
sales_order_repo = SalesOrderRepository()


def list_production_orders(
    session: Session,
    *,
    status: ProductionOrderStatus | str | None = None,
) -> list[ProductionOrder]:
    """Return production orders optionally filtered by status."""

    filters = None
    if status is not None:
        desired_status = (
            status
            if isinstance(status, ProductionOrderStatus)
            else ProductionOrderStatus(status)
        )
        filters = [ProductionOrder.status == desired_status]

    return production_repo.list(session, filters=filters)


def start_production_for_order(session: Session, sales_order_id: int) -> ProductionOrder:
    """Create a production order for the sales order and move it to in_production."""

    order = sales_order_repo.get_or_raise(session, sales_order_id)
    if order.status != SalesOrderStatus.created:
        raise InvalidTransitionError(
            "SalesOrder",
            order.status,
            SalesOrderStatus.in_production,
        )

    try:
        production = production_repo.create(
            session,
            {
                "sales_order_id": order.id,
                "status": ProductionOrderStatus.planned,
            },
        )
        sales_order_repo.update_status(session, order.id, SalesOrderStatus.in_production)
        logger.info(
            "Production order %s created for sales order %s",
            production.id,
            sales_order_id,
        )
        return production_repo.get_or_raise(session, production.id)
    except Exception:
        session.rollback()
        logger.exception("Failed to start production for order %s", sales_order_id)
        raise


def mark_production_in_progress(session: Session, production_id: int) -> ProductionOrder:
    """Set the production order status to in_progress and stamp the start time."""

    production = production_repo.get_or_raise(session, production_id)
    if production.status != ProductionOrderStatus.planned:
        raise InvalidTransitionError(
            "ProductionOrder",
            production.status,
            ProductionOrderStatus.in_progress,
        )

    start_time = current_utc_time()
    updated = production_repo.update(
        session,
        production_id,
        {
            "status": ProductionOrderStatus.in_progress,
            "start_date": start_time,
        },
    )
    logger.info("Production order %s marked in_progress", production_id)
    return updated


def mark_production_complete(session: Session, production_id: int) -> ProductionOrder:
    """Finalize production, set end date, and advance the sales order."""

    production = production_repo.get_or_raise(session, production_id)
    if production.status != ProductionOrderStatus.in_progress:
        raise InvalidTransitionError(
            "ProductionOrder",
            production.status,
            ProductionOrderStatus.completed,
        )

    end_time = current_utc_time()
    updated = production_repo.update(
        session,
        production_id,
        {
            "status": ProductionOrderStatus.completed,
            "end_date": end_time,
        },
    )
    sales_order_repo.update_status(
        session,
        production.sales_order_id,
        SalesOrderStatus.ready_for_delivery,
    )
    logger.info(
        "Production order %s completed; sales order %s ready for delivery",
        production_id,
        production.sales_order_id,
    )
    return updated
