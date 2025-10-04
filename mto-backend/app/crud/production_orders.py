from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import ProductionOrder, ProductionStatus
from app.schemas.production_order import ProductionOrderCreate, ProductionOrderUpdate


def generate_production_number(db: Session) -> str:
    """Generate unique production order number."""
    last_order = db.query(ProductionOrder).order_by(ProductionOrder.id.desc()).first()
    if last_order:
        last_num = int(last_order.order_number.split("-")[1])
        return f"PO-{last_num + 1:06d}"
    return "PO-000001"


def create_production_order(db: Session, order: ProductionOrderCreate) -> ProductionOrder:
    order_number = generate_production_number(db)
    
    db_order = ProductionOrder(
        order_number=order_number,
        sales_order_id=order.sales_order_id,
        product_name=order.product_name,
        quantity=order.quantity,
        status=ProductionStatus.PLANNED
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_production_order(db: Session, order_id: int) -> Optional[ProductionOrder]:
    return db.query(ProductionOrder).filter(ProductionOrder.id == order_id).first()


def get_production_orders(db: Session, skip: int = 0, limit: int = 100) -> List[ProductionOrder]:
    return db.query(ProductionOrder).offset(skip).limit(limit).all()


def update_production_order(db: Session, order_id: int, order_update: ProductionOrderUpdate) -> Optional[ProductionOrder]:
    db_order = get_production_order(db, order_id)
    if not db_order:
        return None
    
    update_data = order_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_production_order(db: Session, order_id: int) -> bool:
    db_order = get_production_order(db, order_id)
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True


