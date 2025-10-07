"""Order service containing multi-entity business workflows."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Any, TypedDict

from sqlmodel import Session

from app.models import SalesOrder, SalesOrderStatus
from app.repositories.billing_repository import BillingRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.production_order_repository import ProductionOrderRepository
from app.repositories.sales_order_item_repository import SalesOrderItemRepository
from app.repositories.sales_order_repository import SalesOrderRepository
from app.services.exceptions import InvalidTransitionError

logger = logging.getLogger(__name__)


class OrderItemInput(TypedDict):
    """Typed mapping describing an incoming order item payload."""

    product_id: int
    quantity: int


product_repo = ProductRepository()
sales_order_repo = SalesOrderRepository()
sales_order_item_repo = SalesOrderItemRepository()
production_repo = ProductionOrderRepository()
delivery_repo = DeliveryRepository()
billing_repo = BillingRepository()
customer_repo = CustomerRepository()


_ALLOWED_TRANSITIONS: dict[SalesOrderStatus, set[SalesOrderStatus]] = {
    SalesOrderStatus.created: {
        SalesOrderStatus.in_production,
        SalesOrderStatus.cancelled,
    },
    SalesOrderStatus.in_production: {
        SalesOrderStatus.ready_for_delivery,
        SalesOrderStatus.cancelled,
    },
    SalesOrderStatus.ready_for_delivery: {
        SalesOrderStatus.delivered,
        SalesOrderStatus.cancelled,
    },
    SalesOrderStatus.delivered: {SalesOrderStatus.billed},
    SalesOrderStatus.cancelled: set(),
    SalesOrderStatus.billed: set(),
}


def get_customer_orders(
    session: Session,
    *,
    status: SalesOrderStatus | str | None = None,
    customer_id: int | None = None,
) -> list[dict[str, Any]]:
    """Return serialized sales order summaries optionally filtered by status and/or customer ID."""

    filters: list[Any] = []
    if status is not None:
        desired_status = (
            status if isinstance(status, SalesOrderStatus) else SalesOrderStatus(status)
        )
        filters.append(SalesOrder.status == desired_status)

    if customer_id is not None:
        filters.append(SalesOrder.customer_id == customer_id)

    orders = sales_order_repo.list(session, filters=filters or None)

    summaries: list[dict[str, Any]] = []
    for order in orders:
        customer = order.customer or customer_repo.get(session, order.customer_id)
        summaries.append(
            {
                "id": order.id,
                "customer_id": order.customer_id,
                "customer_name": getattr(customer, "name", None),
                "status": order.status,
                "total_amount": order.total_amount,
                "created_at": order.created_at,
            }
        )

    return summaries


def create_order_with_items(
    session: Session,
    customer_id: int,
    items: Sequence[OrderItemInput],
) -> SalesOrder:
    """Create a sales order together with its items and return the persisted entity."""

    if not items:
        raise ValueError("At least one item is required to create an order.")

    order_items: list[dict[str, Any]] = []
    total_amount = 0.0

    try:
        for item in items:
            # Handle both dict and object inputs
            if isinstance(item, dict):
                quantity = item["quantity"]
                product_id = item["product_id"]
            else:
                # Handle Pydantic model objects
                quantity = getattr(item, "quantity", 0)
                product_id = getattr(item, "product_id", 0)

            if quantity <= 0:
                raise ValueError("Item quantity must be greater than zero.")

            product = product_repo.get_or_raise(session, product_id)
            subtotal = product.price * quantity
            total_amount += subtotal
            order_items.append(
                {
                    "product_id": product.id,
                    "quantity": quantity,
                    "subtotal": subtotal,
                }
            )

        order = sales_order_repo.create(
            session,
            {
                "customer_id": customer_id,
                "total_amount": total_amount,
                "status": SalesOrderStatus.created,
            },
        )

        for item_payload in order_items:
            sales_order_item_repo.create(
                session,
                {
                    "sales_order_id": order.id,
                    **item_payload,
                },
            )

        logger.info("Created order %s with %d item(s)", order.id, len(order_items))
        return sales_order_repo.get_or_raise(session, order.id)
    except Exception:
        session.rollback()
        logger.exception("Failed to create order for customer %s", customer_id)
        raise


def get_order_details(session: Session, order_id: int) -> dict[str, Any]:
    """Return a composed, serialisable view of the sales order and related records."""

    order = sales_order_repo.get_or_raise(session, order_id)
    customer = order.customer or customer_repo.get(session, order.customer_id)

    items = sales_order_item_repo.list_by_order(session, order_id)
    item_payloads: list[dict[str, Any]] = []
    for item in items:
        product = product_repo.get(session, item.product_id)
        item_payloads.append(
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": getattr(product, "name", None),
                "quantity": item.quantity,
                "subtotal": item.subtotal,
            }
        )

    production_orders = production_repo.list_by_sales_order(session, order_id)
    production_payloads = [
        {
            "id": production.id,
            "status": production.status,
            "start_date": production.start_date,
            "end_date": production.end_date,
        }
        for production in production_orders
    ]

    deliveries = delivery_repo.list_by_sales_order(session, order_id)
    delivery_payloads = [
        {
            "id": delivery.id,
            "status": delivery.status,
            "delivery_date": delivery.delivery_date,
        }
        for delivery in deliveries
    ]

    billing = billing_repo.get_by_sales_order(session, order_id)
    billing_payload = (
        {
            "id": billing.id,
            "invoice_number": billing.invoice_number,
            "amount": billing.amount,
            "billed_date": billing.billed_date,
        }
        if billing
        else None
    )

    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "customer_name": getattr(customer, "name", None),
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "items": item_payloads,
        "production_orders": production_payloads,
        "deliveries": delivery_payloads,
        "billing": billing_payload,
    }


def update_order_status(
    session: Session,
    order_id: int,
    status: SalesOrderStatus | str,
) -> SalesOrder:
    """Transition an order to a new status if the change is allowed."""

    desired_status = (
        status
        if isinstance(status, SalesOrderStatus)
        else SalesOrderStatus(status)
    )
    order = sales_order_repo.get_or_raise(session, order_id)

    allowed_targets = _ALLOWED_TRANSITIONS.get(order.status, set())
    if desired_status not in allowed_targets:
        raise InvalidTransitionError(
            "SalesOrder",
            order.status,
            desired_status,
        )

    updated = sales_order_repo.update_status(session, order_id, desired_status)
    logger.info(
        "Order %s transitioned from %s to %s",
        order_id,
        order.status,
        desired_status,
    )
    return updated


def delete_order(session: Session, order_id: int) -> bool:
    """Delete an order and all its associated items."""

    # Ensure the order exists before attempting deletions.
    sales_order_repo.get_or_raise(session, order_id)
    items = sales_order_item_repo.list_by_order(session, order_id)

    try:
        for item in items:
            sales_order_item_repo.delete(session, item.id)
        deleted = sales_order_repo.delete(session, order_id)
        logger.info("Deleted order %s and %d item(s)", order_id, len(items))
        return deleted
    except Exception:
        session.rollback()
        logger.exception("Failed to delete order %s", order_id)
        raise
