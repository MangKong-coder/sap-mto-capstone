import enum
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum as SAEnum,
    func, DDL, event
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False,
                        default=func.now(), onupdate=func.now())

# Enums for statuses

class OrderStatus(enum.Enum):
    NEW = "NEW"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class CustomerTypes(enum.Enum):
    DEPARTMENT = "DEPARTMENT"
    CAMPUS = "CAMPUS"
    STUDENT = "STUDENT"
    VENDOR = "VENDOR"

class OrderPriorities(enum.Enum):
    STANDARD = "STANDARD"
    URGENT = "URGENT"
    RUSH = "RUSH"

class PlannedOrderStatus(enum.Enum):
    PLANNED = "PLANNED"
    CONVERTED = "CONVERTED"
    CANCELLED = "CANCELLED"

class WorkOrderStatus(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

class DeliveryStatus(enum.Enum):
    PENDING = "PENDING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class InvoiceStatus(enum.Enum):
    DRAFT = "DRAFT"
    POSTED = "POSTED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


# Core tables

class Customer(TimestampMixin, Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200))
    phone = Column(String(50))
    address = Column(Text)
    customer_type = Column(SAEnum(CustomerTypes, name="customer_types"), nullable=False, default=CustomerTypes.DEPARTMENT)

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")


class Product(TimestampMixin, Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False, default=0.0)

    order_items = relationship("OrderItem", back_populates="product")


class WorkCenter(TimestampMixin, Base):
    __tablename__ = "work_centers"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    address = Column(Text)

    orders = relationship("Order", back_populates="work_center")

class Order(TimestampMixin, Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    status = Column(SAEnum(OrderStatus, name="order_status"), nullable=False, default=OrderStatus.NEW)
    order_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    delivery_date = Column(DateTime(timezone=True))
    priority = Column(SAEnum(OrderPriorities, name="order_priority"), nullable=False, default=OrderPriorities.STANDARD)
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    planned_orders = relationship("PlannedOrder", back_populates="order")
    deliveries = relationship("Delivery", back_populates="order")
    invoices = relationship("Invoice", back_populates="order")
    work_center_id = Column(Integer, ForeignKey("work_centers.id", ondelete="RESTRICT"), nullable=False)
    work_center = relationship("WorkCenter", back_populates="orders")


class OrderItem(TimestampMixin, Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Float, nullable=False, default=1.0)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    planned_orders = relationship("PlannedOrder", back_populates="order_item")
    work_orders = relationship("WorkOrder", back_populates="order_item", cascade="all, delete-orphan")


class PlannedOrder(TimestampMixin, Base):
    """
    A “planned” production based on sales demand, before conversion to a work (production) order.
    """
    __tablename__ = "planned_orders"
    id = Column(Integer, primary_key=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Float, nullable=False)
    status = Column(SAEnum(PlannedOrderStatus, name="planned_order_status"), nullable=False, default=PlannedOrderStatus.PLANNED)
    planned_start = Column(DateTime(timezone=True))
    planned_end = Column(DateTime(timezone=True))

    order_item = relationship("OrderItem", back_populates="planned_orders")
    order = relationship("Order", back_populates="planned_orders")
    # After conversion, we might link to WorkOrder(s)
    work_order = relationship("WorkOrder", uselist=False, back_populates="planned_order")


class WorkOrder(TimestampMixin, Base):
    __tablename__ = "work_orders"
    id = Column(Integer, primary_key=True)
    planned_order_id = Column(Integer, ForeignKey("planned_orders.id", ondelete="SET NULL"), nullable=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Float, nullable=False)
    status = Column(SAEnum(WorkOrderStatus, name="work_order_status"), nullable=False, default=WorkOrderStatus.PENDING)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))

    planned_order = relationship("PlannedOrder", back_populates="work_order")
    order_item = relationship("OrderItem", back_populates="work_orders")
    component_usages = relationship("ComponentUsage", back_populates="work_order", cascade="all, delete-orphan")


class Component(TimestampMixin, Base):
    __tablename__ = "components"
    id = Column(Integer, primary_key=True)
    part_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    cost = Column(Float, nullable=False, default=0.0)

    usages = relationship("ComponentUsage", back_populates="component", cascade="all, delete-orphan")


class ComponentUsage(TimestampMixin, Base):
    __tablename__ = "component_usages"
    id = Column(Integer, primary_key=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=False)
    component_id = Column(Integer, ForeignKey("components.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Float, nullable=False)

    work_order = relationship("WorkOrder", back_populates="component_usages")
    component = relationship("Component", back_populates="usages")


class Delivery(TimestampMixin, Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    delivered_at = Column(DateTime(timezone=True))
    status = Column(SAEnum(DeliveryStatus, name="delivery_status"), nullable=False, default=DeliveryStatus.PENDING)
    quantity = Column(Float, nullable=False)

    order = relationship("Order", back_populates="deliveries")


class Invoice(TimestampMixin, Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    invoice_date = Column(DateTime(timezone=True))
    status = Column(SAEnum(InvoiceStatus, name="invoice_status"), nullable=False, default=InvoiceStatus.DRAFT)
    total_amount = Column(Float, nullable=False)

    order = relationship("Order", back_populates="invoices")


# View: aggregated component usage per order, via a view

view_ddl = DDL("""
CREATE OR REPLACE VIEW vw_order_component_usage AS
  SELECT
    o.id AS order_id,
    cu.component_id,
    SUM(cu.quantity) AS total_used
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.id
  JOIN work_orders wo ON wo.order_item_id = oi.id
  JOIN component_usages cu ON cu.work_order_id = wo.id
  GROUP BY o.id, cu.component_id;
""")

drop_view_ddl = DDL("DROP VIEW IF EXISTS vw_order_component_usage;")

event.listen(Base.metadata, "after_create", view_ddl)
event.listen(Base.metadata, "before_drop", drop_view_ddl)

# Optional: map the view as a read-only model
from sqlalchemy import Table

class OrderComponentUsage(Base):
    __tablename__ = "vw_order_component_usage"
    __table__ = Table(
        __tablename__, Base.metadata,
        Column("order_id", Integer, primary_key=True),
        Column("component_id", Integer, primary_key=True),
        Column("total_used", Float),
    )
    # Read-only; no relationships by default
