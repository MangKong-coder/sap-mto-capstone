from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import SalesOrder, OrderStatus
from app.schemas.sales_order import SalesOrderCreate, SalesOrderUpdate


def generate_order_number(db: Session) -> str:
    """Generate unique sales order number."""
    last_order = db.query(SalesOrder).order_by(SalesOrder.id.desc()).first()
    if last_order:
        last_num = int(last_order.order_number.split("-")[1])
        return f"SO-{last_num + 1:06d}"
    return "SO-000001"


def create_sales_order(db: Session, order: SalesOrderCreate) -> SalesOrder:
    total_amount = order.quantity * order.unit_price
    order_number = generate_order_number(db)
    
    db_order = SalesOrder(
        order_number=order_number,
        customer_name=order.customer_name,
        product_name=order.product_name,
        quantity=order.quantity,
        unit_price=order.unit_price,
        total_amount=total_amount,
        status=OrderStatus.PENDING
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_sales_order(db: Session, order_id: int) -> Optional[SalesOrder]:
    return db.query(SalesOrder).filter(SalesOrder.id == order_id).first()


def get_sales_orders(db: Session, skip: int = 0, limit: int = 100) -> List[SalesOrder]:
    return db.query(SalesOrder).offset(skip).limit(limit).all()


def update_sales_order(db: Session, order_id: int, order_update: SalesOrderUpdate) -> Optional[SalesOrder]:
    db_order = get_sales_order(db, order_id)
    if not db_order:
        return None
    
    update_data = order_update.model_dump(exclude_unset=True)
    
    # Recalculate total if quantity or unit_price changed
    if "quantity" in update_data or "unit_price" in update_data:
        quantity = update_data.get("quantity", db_order.quantity)
        unit_price = update_data.get("unit_price", db_order.unit_price)
        update_data["total_amount"] = quantity * unit_price
    
    for key, value in update_data.items():
        setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_sales_order(db: Session, order_id: int) -> bool:
    db_order = get_sales_order(db, order_id)
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True

