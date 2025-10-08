from datetime import UTC, datetime
from typing import List, Optional

import enum
from sqlmodel import Field, Relationship, SQLModel


def current_utc_time() -> datetime:
    """Return the current time with UTC timezone information."""
    return datetime.now(UTC)


class SalesOrderStatus(str, enum.Enum):
    created = "created"
    in_production = "in_production"
    ready_for_delivery = "ready_for_delivery"
    delivered = "delivered"
    billed = "billed"
    cancelled = "cancelled"


class ProductionOrderStatus(str, enum.Enum):
    planned = "planned"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class DeliveryStatus(str, enum.Enum):
    pending = "pending"
    delivered = "delivered"
    cancelled = "cancelled"

# --- Customers ---
class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    role: str  # student, faculty, department
    orders: List["SalesOrder"] = Relationship(back_populates="customer")

# --- Products ---
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    image_url: Optional[str] = None

# --- Sales Orders ---
class SalesOrder(SQLModel, table=True):
    __tablename__ = "sales_order"
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    total_amount: float
    status: SalesOrderStatus = Field(default=SalesOrderStatus.created)
    created_at: datetime = Field(default_factory=current_utc_time)

    customer: Optional[Customer] = Relationship(back_populates="orders")
    items: List["SalesOrderItem"] = Relationship(back_populates="sales_order")
    production: Optional["ProductionOrder"] = Relationship(back_populates="sales_order")
    delivery: Optional["Delivery"] = Relationship(back_populates="sales_order")
    billing: Optional["Billing"] = Relationship(back_populates="sales_order")

# --- Sales Order Items ---
class SalesOrderItem(SQLModel, table=True):
    __tablename__ = "sales_order_item"
    id: Optional[int] = Field(default=None, primary_key=True)
    sales_order_id: int = Field(foreign_key="sales_order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    subtotal: float

    sales_order: Optional[SalesOrder] = Relationship(back_populates="items")

# --- Production Order ---
class ProductionOrder(SQLModel, table=True):
    __tablename__ = "production_order"
    id: Optional[int] = Field(default=None, primary_key=True)
    sales_order_id: int = Field(foreign_key="sales_order.id")
    status: ProductionOrderStatus = Field(default=ProductionOrderStatus.planned)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    sales_order: Optional[SalesOrder] = Relationship(back_populates="production")

# --- Delivery ---
class Delivery(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sales_order_id: int = Field(foreign_key="sales_order.id")
    delivery_date: Optional[datetime] = None
    status: DeliveryStatus = Field(default=DeliveryStatus.pending)

    sales_order: Optional[SalesOrder] = Relationship(back_populates="delivery")

# --- Billing ---
class Billing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sales_order_id: int = Field(foreign_key="sales_order.id")
    invoice_number: Optional[str] = None
    amount: float
    billed_date: Optional[datetime] = Field(default_factory=current_utc_time)

    sales_order: Optional[SalesOrder] = Relationship(back_populates="billing")
