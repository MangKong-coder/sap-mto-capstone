from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import SalesOrder, SalesOrderItem, Customer, Product

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.get("/")
def list_orders(session: Session = Depends(get_session)):
    orders = session.exec(select(SalesOrder)).all()
    return orders

@router.post("/")
def create_order(customer_id: int, items: list[dict], session: Session = Depends(get_session)):
    total = 0
    for item in items:
        product = session.get(Product, item["product_id"])
        total += product.price * item["quantity"]

    order = SalesOrder(customer_id=customer_id, total_amount=total)
    session.add(order)
    session.commit()
    session.refresh(order)

    for item in items:
        product = session.get(Product, item["product_id"])
        session.add(SalesOrderItem(
            sales_order_id=order.id,
            product_id=product.id,
            quantity=item["quantity"],
            subtotal=product.price * item["quantity"]
        ))
    session.commit()
    return {"message": "Order created", "order_id": order.id, "total": total}
