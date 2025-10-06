"""Delivery service orchestrating fulfillment workflows."""

from __future__ import annotations

import logging
from datetime import datetime

from sqlmodel import Session

from app.models import Delivery, DeliveryStatus, SalesOrderStatus, current_utc_time
from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.sales_order_repository import SalesOrderRepository
from app.services.exceptions import InvalidTransitionError

logger = logging.getLogger(__name__)

delivery_repo = DeliveryRepository()
sales_order_repo = SalesOrderRepository()


def create_delivery_for_order(
    session: Session,
    sales_order_id: int,
    delivery_date: datetime | None = None,
) -> Delivery:
    """Create a delivery record for a sales order that is ready for delivery."""

    order = sales_order_repo.get_or_raise(session, sales_order_id)
    if order.status != SalesOrderStatus.ready_for_delivery:
        raise InvalidTransitionError(
            "SalesOrder",
            order.status,
            SalesOrderStatus.ready_for_delivery,
        )

    try:
        delivery = delivery_repo.create(
            session,
            {
                "sales_order_id": order.id,
                "status": DeliveryStatus.pending,
                "delivery_date": delivery_date,
            },
        )
        logger.info(
            "Created delivery %s for sales order %s",
            delivery.id,
            sales_order_id,
        )
        return delivery
    except Exception:
        session.rollback()
        logger.exception("Failed to create delivery for order %s", sales_order_id)
        raise


def mark_delivery_done(session: Session, delivery_id: int) -> Delivery:
    """Mark the delivery as delivered and update the linked sales order."""

    delivery = delivery_repo.get_or_raise(session, delivery_id)
    if delivery.status != DeliveryStatus.pending:
        raise InvalidTransitionError(
            "Delivery",
            delivery.status,
            DeliveryStatus.delivered,
        )

    completion_time = current_utc_time()
    updated = delivery_repo.update(
        session,
        delivery_id,
        {
            "status": DeliveryStatus.delivered,
            "delivery_date": completion_time,
        },
    )
    sales_order_repo.update_status(
        session,
        delivery.sales_order_id,
        SalesOrderStatus.delivered,
    )
    logger.info(
        "Delivery %s marked delivered for sales order %s",
        delivery_id,
        delivery.sales_order_id,
    )
    return updated
