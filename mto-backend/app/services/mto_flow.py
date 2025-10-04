"""
MTO Flow Service - Business logic for make-to-order flow.
Handles automatic creation of production orders from sales orders, etc.
"""

from sqlalchemy.orm import Session

from app.crud import sales_orders, production_orders
from app.models import SalesOrder, ProductionOrder
from app.schemas.production_order import ProductionOrderCreate


def auto_create_production_order(db: Session, sales_order: SalesOrder) -> ProductionOrder:
    """
    Automatically create a production order from a sales order.
    This is called after a sales order is confirmed.
    """
    production_order_data = ProductionOrderCreate(
        sales_order_id=sales_order.id,
        product_name=sales_order.product_name,
        quantity=sales_order.quantity
    )
    return production_orders.create_production_order(db, production_order_data)


