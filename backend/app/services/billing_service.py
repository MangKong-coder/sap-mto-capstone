"""Billing service handling invoicing workflows."""

from __future__ import annotations

import logging
import secrets
from datetime import UTC, datetime

from sqlmodel import Session

from app.models import Billing, SalesOrderStatus
from app.repositories.billing_repository import BillingRepository
from app.repositories.sales_order_repository import SalesOrderRepository
from app.services.exceptions import InvalidTransitionError

logger = logging.getLogger(__name__)

billing_repo = BillingRepository()
sales_order_repo = SalesOrderRepository()


def _generate_invoice_number(timestamp: datetime) -> str:
    """Return an invoice number following the `INV-{YYYY}-{random4}` format."""

    random_suffix = f"{secrets.randbelow(10000):04d}"
    return f"INV-{timestamp:%Y}-{random_suffix}"


def generate_billing_for_order(session: Session, sales_order_id: int) -> Billing:
    """Create a billing record for a delivered sales order and mark it billed."""

    order = sales_order_repo.get_or_raise(session, sales_order_id)
    existing = billing_repo.get_by_sales_order(session, sales_order_id)
    if existing is not None:
        return existing

    if order.status != SalesOrderStatus.delivered:
        raise InvalidTransitionError(
            "SalesOrder",
            order.status,
            SalesOrderStatus.billed,
        )

    billed_at = datetime.now(tz=UTC)
    invoice_number = _generate_invoice_number(billed_at)

    try:
        billing = billing_repo.create(
            session,
            {
                "sales_order_id": sales_order_id,
                "invoice_number": invoice_number,
                "amount": order.total_amount,
                "billed_date": billed_at,
            },
        )
        sales_order_repo.update_status(session, sales_order_id, SalesOrderStatus.billed)
        logger.info(
            "Generated invoice %s for sales order %s",
            billing.invoice_number,
            sales_order_id,
        )
        return billing
    except Exception:
        session.rollback()
        logger.exception("Failed to generate billing for order %s", sales_order_id)
        raise


def get_billing_for_order(session: Session, sales_order_id: int) -> Billing | None:
    """Return the billing record for the specified sales order, if any."""

    return billing_repo.get_by_sales_order(session, sales_order_id)
