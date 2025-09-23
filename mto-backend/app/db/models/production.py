from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from app.db.base_class import TimestampMixin


class ProductionOrder(Base, TimestampMixin):
    __tablename__ = "production_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    planned_quantity = Column(Integer, nullable=False)
    status = Column(String, default="created")  # created, in_progress, done
    scheduled_date = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="production_orders")
    product = relationship("Product")


class WorkCenter(Base, TimestampMixin):
    __tablename__ = "work_centers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, default=1)  # e.g., number of machines or operators

    routing_steps = relationship("RoutingStep", back_populates="work_center")


class RoutingStep(Base, TimestampMixin):
    __tablename__ = "routing_steps"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    work_center_id = Column(Integer, ForeignKey("work_centers.id"))
    step_number = Column(Integer, nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer, default=0)

    product = relationship("Product", back_populates="routings")
    work_center = relationship("WorkCenter", back_populates="routing_steps")
