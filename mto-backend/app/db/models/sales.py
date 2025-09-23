from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from app.db.base_class import TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False, default=0.00)

    order_items = relationship("OrderItem", back_populates="product")
    routings = relationship("RoutingStep", back_populates="product")


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, confirmed, shipped, etc.

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    production_orders = relationship("ProductionOrder", back_populates="order")


class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
