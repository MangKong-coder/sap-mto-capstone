from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Delivery, DeliveryStatus
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate


def generate_delivery_number(db: Session) -> str:
    """Generate unique delivery number."""
    last_delivery = db.query(Delivery).order_by(Delivery.id.desc()).first()
    if last_delivery:
        last_num = int(last_delivery.delivery_number.split("-")[1])
        return f"DL-{last_num + 1:06d}"
    return "DL-000001"


def create_delivery(db: Session, delivery: DeliveryCreate) -> Delivery:
    delivery_number = generate_delivery_number(db)
    
    db_delivery = Delivery(
        delivery_number=delivery_number,
        production_order_id=delivery.production_order_id,
        sales_order_id=delivery.sales_order_id,
        quantity=delivery.quantity,
        status=DeliveryStatus.PENDING
    )
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery


def get_delivery(db: Session, delivery_id: int) -> Optional[Delivery]:
    return db.query(Delivery).filter(Delivery.id == delivery_id).first()


def get_deliveries(db: Session, skip: int = 0, limit: int = 100) -> List[Delivery]:
    return db.query(Delivery).offset(skip).limit(limit).all()


def update_delivery(db: Session, delivery_id: int, delivery_update: DeliveryUpdate) -> Optional[Delivery]:
    db_delivery = get_delivery(db, delivery_id)
    if not db_delivery:
        return None
    
    update_data = delivery_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_delivery, key, value)
    
    db.commit()
    db.refresh(db_delivery)
    return db_delivery


def delete_delivery(db: Session, delivery_id: int) -> bool:
    db_delivery = get_delivery(db, delivery_id)
    if not db_delivery:
        return False
    db.delete(db_delivery)
    db.commit()
    return True

