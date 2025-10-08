"""Billing service handling invoicing workflows."""

from __future__ import annotations

import base64
import logging
import os
import secrets
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Sequence

import resend
from fpdf import FPDF
from sqlmodel import Session

from app.models import Billing, SalesOrderStatus
from app.repositories.billing_repository import BillingRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.sales_order_item_repository import SalesOrderItemRepository
from app.repositories.sales_order_repository import SalesOrderRepository
from app.services.exceptions import EmailDeliveryError, InvalidTransitionError

if TYPE_CHECKING:
    from app.models import Customer, SalesOrder

logger = logging.getLogger(__name__)

billing_repo = BillingRepository()
sales_order_repo = SalesOrderRepository()
sales_order_item_repo = SalesOrderItemRepository()
customer_repo = CustomerRepository()
product_repo = ProductRepository()


def list_billings(session: Session) -> Sequence[Billing]:
    """Return all billing records."""

    return billing_repo.list(session)


def get_billing(session: Session, billing_id: int) -> Billing:
    """Return a billing record by its identifier or raise if missing."""

    return billing_repo.get_or_raise(session, billing_id)


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


def generate_billing_and_send_invoice(session: Session, sales_order_id: int) -> Billing:
    """Create or retrieve billing for a sales order and send the invoice via email."""

    billing = generate_billing_for_order(session, sales_order_id)
    order = sales_order_repo.get_or_raise(session, sales_order_id)
    customer = order.customer or customer_repo.get(session, order.customer_id)
    if customer is None:
        raise ValueError(f"Customer {order.customer_id} not found for sales order {order.id}.")

    items = sales_order_item_repo.list_by_order(session, sales_order_id)
    line_items: list[dict[str, str | int | float]] = []
    for item in items:
        product = product_repo.get(session, item.product_id)
        product_name = getattr(product, "name", f"Product #{item.product_id}")
        line_items.append(
            {
                "name": product_name,
                "quantity": item.quantity,
                "subtotal": item.subtotal,
            }
        )

    pdf_bytes = _build_invoice_pdf(billing, order, customer, line_items)

    try:
        _send_invoice_email(billing, order, customer, pdf_bytes)
    except EmailDeliveryError:
        raise
    except Exception as exc:  # pragma: no cover - unexpected errors should be surfaced
        logger.exception("Unexpected error while sending invoice email for order %s", order.id)
        raise EmailDeliveryError("Failed to send invoice email.") from exc

    return billing


def _build_invoice_pdf(
    billing: Billing,
    order: "SalesOrder",
    customer: "Customer",
    line_items: Sequence[dict[str, str | int | float]],
) -> bytes:
    """Return a PDF document containing invoice details as bytes."""

    billed_at = billing.billed_date or datetime.now(tz=UTC)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Invoice", ln=True)

    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 8, f"Invoice Number: {billing.invoice_number}", ln=True)
    pdf.cell(0, 8, f"Invoice Date: {billed_at:%Y-%m-%d %H:%M %Z}", ln=True)
    pdf.ln(4)
    pdf.cell(0, 8, f"Bill To: {customer.name}", ln=True)
    pdf.cell(0, 8, f"Email: {customer.email}", ln=True)
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(100, 8, "Item", border=1)
    pdf.cell(30, 8, "Quantity", border=1, align="R")
    pdf.cell(40, 8, "Subtotal", border=1, align="R", ln=True)

    pdf.set_font("Helvetica", size=12)
    for entry in line_items:
        pdf.cell(100, 8, str(entry["name"]), border=1)
        pdf.cell(30, 8, f"{entry['quantity']}", border=1, align="R")
        pdf.cell(40, 8, f"{entry['subtotal']:.2f}", border=1, align="R", ln=True)

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(130, 8, "Total", border=1)
    pdf.cell(40, 8, f"{billing.amount:.2f}", border=1, align="R", ln=True)

    output = pdf.output(dest="S")
    return output


def _send_invoice_email(
    billing: Billing,
    order: "SalesOrder",
    customer: "Customer",
    pdf_bytes: bytes,
) -> None:
    """Send the generated invoice PDF via Resend email service."""

    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        raise EmailDeliveryError("RESEND_API_KEY environment variable is not set.")

    sender = os.getenv("BILLING_FROM_EMAIL")
    if not sender:
        raise EmailDeliveryError("BILLING_FROM_EMAIL environment variable is not set.")

    if not customer.email:
        raise EmailDeliveryError("Customer email address is missing.")

    resend.api_key = api_key

    attachment_b64 = base64.b64encode(pdf_bytes).decode("ascii")
    subject = f"Invoice {billing.invoice_number} for Sales Order #{order.id}"
    html_body = _render_invoice_email_html(billing, customer)

    try:
        resend.Emails.send(
            {
                "from": sender,
                "to": [customer.email],
                "subject": subject,
                "html": html_body,
                "attachments": [
                    {
                        "filename": f"{billing.invoice_number}.pdf",
                        "content": attachment_b64,
                        "content_type": "application/pdf",
                    }
                ],
            }
        )
    except Exception as exc:  # pragma: no cover - depends on external service
        raise EmailDeliveryError("Resend failed to send the invoice email.") from exc
    logger.info(
        "Sent invoice %s to %s for sales order %s",
        billing.invoice_number,
        customer.email,
        order.id,
    )


def _render_invoice_email_html(billing: Billing, customer: "Customer") -> str:
    """Return HTML body for invoice email."""

    amount_formatted = f"{billing.amount:,.2f}"
    greeting_name = customer.name or "valued customer"
    return (
        f"<p>Dear {greeting_name},</p>"
        f"<p>Thank you for your order. Please find your invoice <strong>{billing.invoice_number}</strong> attached."  # noqa: E501
        "</p>"
        f"<p><strong>Amount Due:</strong> {amount_formatted}</p>"
        "<p>Please settle the payment at your earliest convenience.</p>"
        "<p>Best regards,<br/>Mapúa MTO Billing Team</p>"
    )
