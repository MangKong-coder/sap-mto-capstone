from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.db.models import Product, Order, OrderItem
from app.schemas.sales import ProductCreate, ProductResponse, OrderCreate, OrderResponse

router = APIRouter()


@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Note: In a real app, you'd get user_id from authentication
    db_order = Order(
        user_id=1,  # Placeholder - should come from auth
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Add order items
    for item in order.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_item)
    
    db.commit()
    return db_order
