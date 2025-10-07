"""Dashboard service providing aggregated KPIs for admin views."""

from __future__ import annotations

from typing import Any, Dict, List

from sqlalchemy import desc, func
from sqlmodel import Session, select

from app.models import (
    Customer,
    Product,
    ProductionOrder,
    ProductionOrderStatus,
    SalesOrder,
    SalesOrderStatus,
    SalesOrderItem,
)


def get_dashboard_summary(session: Session) -> Dict[str, Any]:
    """Return aggregated statistics for the dashboard summary endpoint."""

    total_orders = session.exec(
        select(func.count()).select_from(SalesOrder)
    ).one()
    in_production = session.exec(
        select(func.count()).select_from(ProductionOrder).where(
            ProductionOrder.status == ProductionOrderStatus.in_progress
        )
    ).one()
    ready_for_delivery = session.exec(
        select(func.count())
        .select_from(SalesOrder)
        .where(SalesOrder.status == SalesOrderStatus.ready_for_delivery)
    ).one()
    billed = session.exec(
        select(func.count())
        .select_from(SalesOrder)
        .where(SalesOrder.status == SalesOrderStatus.billed)
    ).one()

    top_products_rows = session.exec(
        select(
            SalesOrderItem.product_id,
            func.sum(SalesOrderItem.quantity).label("orders"),
        )
        .group_by(SalesOrderItem.product_id)
        .order_by(desc("orders"))
        .limit(5)
    ).all()

    product_ids = [row.product_id for row in top_products_rows]
    product_names: Dict[int, str] = {}
    if product_ids:
        product_name_rows = session.exec(
            select(Product.id, Product.name).where(Product.id.in_(product_ids))
        ).all()
        product_names = {row.id: row.name for row in product_name_rows}

    top_products: List[Dict[str, Any]] = [
        {
            "product_id": row.product_id,
            "name": product_names.get(row.product_id),
            "orders": int(row.orders or 0),
        }
        for row in top_products_rows
    ]

    recent_orders = session.exec(
        select(
            SalesOrder.id,
            SalesOrder.total_amount,
            SalesOrder.status,
            SalesOrder.created_at,
            Customer.name.label("customer_name"),
        )
        .join(Customer, SalesOrder.customer_id == Customer.id)
        .order_by(desc(SalesOrder.created_at))
        .limit(5)
    ).all()

    recent_orders_data = [
        {
            "id": row.id,
            "customer_name": row.customer_name,
            "status": row.status,
            "total_amount": float(row.total_amount or 0),
            "created_at": row.created_at,
        }
        for row in recent_orders
    ]

    return {
        "total_orders": int(total_orders or 0),
        "in_production": int(in_production or 0),
        "ready_for_delivery": int(ready_for_delivery or 0),
        "billed": int(billed or 0),
        "top_products": top_products,
        "recent_orders": recent_orders_data,
    }
