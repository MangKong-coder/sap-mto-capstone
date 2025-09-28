from typing import Optional
import datetime
import decimal
from enum import Enum


from sqlalchemy import Boolean, CHAR, CheckConstraint, Column, DateTime, Enum as PgEnum, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlmodel import Field, Relationship, SQLModel


# Enums
class OrderStatus(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    FULFILLED = "FULFILLED"


class ProductionOrderStatus(str, Enum):
    PLANNED = "PLANNED"
    RELEASED = "RELEASED"
    IN_PROCESS = "IN_PROCESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class OperationStatus(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    STARTED = "STARTED"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"


class DeliveryStatus(str, Enum):
    DRAFT = "DRAFT"
    PACKED = "PACKED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class InventoryMovementType(str, Enum):
    GOODS_ISSUE = "GOODS_ISSUE"
    GOODS_RECEIPT = "GOODS_RECEIPT"
    ADJUSTMENT = "ADJUSTMENT"
    RESERVATION = "RESERVATION"
    RELEASE_RESERVATION = "RELEASE_RESERVATION"


class UoM(str, Enum):
    EA = "EA"
    HOUR = "HOUR"
    KG = "KG"
    M = "M"

# Models

class Customers(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint('id', name='customers_pkey'),
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    name: str = Field(sa_column=Column('name', String(150), nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    code: Optional[str] = Field(default=None, sa_column=Column('code', String(32)))
    email: Optional[str] = Field(default=None, sa_column=Column('email', String(254)))
    phone: Optional[str] = Field(default=None, sa_column=Column('phone', String(32)))
    address_line1: Optional[str] = Field(default=None, sa_column=Column('address_line1', String(200)))
    address_line2: Optional[str] = Field(default=None, sa_column=Column('address_line2', String(200)))
    city: Optional[str] = Field(default=None, sa_column=Column('city', String(100)))
    region: Optional[str] = Field(default=None, sa_column=Column('region', String(100)))
    postal_code: Optional[str] = Field(default=None, sa_column=Column('postal_code', String(20)))
    country: Optional[str] = Field(default=None, sa_column=Column('country', CHAR(2), server_default=text("'PH'::bpchar")))

    sales_orders: list['SalesOrders'] = Relationship(back_populates='customer')


class Products(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint('id', name='products_pkey'),
        UniqueConstraint('sku', name='products_sku_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    name: str = Field(sa_column=Column('name', String(150), nullable=False))
    sku: str = Field(sa_column=Column('sku', String(64), nullable=False))
    unit_of_measure: str = Field(sa_column=Column('unit_of_measure', PgEnum('EA', 'HOUR', 'KG', 'M', name='uom_enum'), nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    description: Optional[str] = Field(default=None, sa_column=Column('description', Text))
    make_to_order: Optional[bool] = Field(default=None, sa_column=Column('make_to_order', Boolean, server_default=text('true')))
    standard_cost: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('standard_cost', Numeric, server_default=text('0')))
    list_price: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('list_price', Numeric, server_default=text('0')))
    is_active: Optional[bool] = Field(default=None, sa_column=Column('is_active', Boolean, server_default=text('true')))

    boms: list['Boms'] = Relationship(back_populates='product')
    inventory_balances: Optional['InventoryBalances'] = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates='product')
    routings: list['Routings'] = Relationship(back_populates='product')
    bom_items: list['BomItems'] = Relationship(back_populates='component_product')
    production_orders: list['ProductionOrders'] = Relationship(back_populates='product')
    sales_order_items: list['SalesOrderItems'] = Relationship(back_populates='product')


class Roles(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint('id', name='roles_pkey'),
        UniqueConstraint('name', name='roles_name_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    name: str = Field(sa_column=Column('name', String(50), nullable=False))

    users: list['Users'] = Relationship(back_populates='role')


class WorkCenters(SQLModel, table=True):
    __tablename__: str = 'work_centers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='work_centers_pkey'),
        UniqueConstraint('name', name='work_centers_name_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    name: str = Field(sa_column=Column('name', String(100), nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    location: Optional[str] = Field(default=None, sa_column=Column('location', String(120)))
    capacity_per_hour: Optional[int] = Field(default=None, sa_column=Column('capacity_per_hour', Integer))
    cost_per_hour: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('cost_per_hour', Numeric))
    is_active: Optional[bool] = Field(default=None, sa_column=Column('is_active', Boolean, server_default=text('true')))

    routing_operations: list['RoutingOperations'] = Relationship(back_populates='work_center')


class Boms(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['product_id'], ['products.id'], name='boms_product_id_fkey'),
        PrimaryKeyConstraint('id', name='boms_pkey'),
        UniqueConstraint('product_id', 'version', name='boms_product_id_version_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    product_id: int = Field(sa_column=Column('product_id', Integer, nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    version: Optional[int] = Field(default=None, sa_column=Column('version', Integer, server_default=text('1')))
    is_active: Optional[bool] = Field(default=None, sa_column=Column('is_active', Boolean, server_default=text('true')))
    effective_from: Optional[datetime.datetime] = Field(default=None, sa_column=Column('effective_from', DateTime(True)))
    effective_to: Optional[datetime.datetime] = Field(default=None, sa_column=Column('effective_to', DateTime(True)))

    product: Optional['Products'] = Relationship(back_populates='boms')
    bom_items: list['BomItems'] = Relationship(back_populates='bom')
    production_orders: list['ProductionOrders'] = Relationship(back_populates='bom')
    sales_order_items: list['SalesOrderItems'] = Relationship(back_populates='bom')


class InventoryBalances(SQLModel, table=True):
    __tablename__: str = 'inventory_balances'
    __table_args__ = (
        ForeignKeyConstraint(['product_id'], ['products.id'], name='inventory_balances_product_id_fkey'),
        PrimaryKeyConstraint('id', name='inventory_balances_pkey'),
        UniqueConstraint('product_id', name='inventory_balances_product_id_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    product_id: int = Field(sa_column=Column('product_id', Integer, nullable=False))
    on_hand: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('on_hand', Numeric, server_default=text('0')))
    reserved: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('reserved', Numeric, server_default=text('0')))

    product: Optional['Products'] = Relationship(back_populates='inventory_balances')


class Routings(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['product_id'], ['products.id'], name='routings_product_id_fkey'),
        PrimaryKeyConstraint('id', name='routings_pkey'),
        UniqueConstraint('product_id', 'version', name='routings_product_id_version_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    product_id: int = Field(sa_column=Column('product_id', Integer, nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    version: Optional[int] = Field(default=None, sa_column=Column('version', Integer, server_default=text('1')))
    is_active: Optional[bool] = Field(default=None, sa_column=Column('is_active', Boolean, server_default=text('true')))

    product: Optional['Products'] = Relationship(back_populates='routings')
    production_orders: list['ProductionOrders'] = Relationship(back_populates='routing')
    routing_operations: list['RoutingOperations'] = Relationship(back_populates='routing')
    sales_order_items: list['SalesOrderItems'] = Relationship(back_populates='routing')


class SalesOrders(SQLModel, table=True):
    __tablename__: str = 'sales_orders'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customers.id'], name='sales_orders_customer_id_fkey'),
        PrimaryKeyConstraint('id', name='sales_orders_pkey'),
        UniqueConstraint('order_no', name='sales_orders_order_no_key')
    )

    id: Optional[int] = Field(sa_column=Column('id', Integer, primary_key=True))
    order_no: str = Field(sa_column=Column('order_no', String(32), nullable=False))
    customer_id: int = Field(sa_column=Column('customer_id', Integer, nullable=False))
    status: str = Field(sa_column=Column('status', PgEnum('DRAFT', 'CONFIRMED', 'CANCELLED', 'FULFILLED', name='order_status_enum'), nullable=False))
    order_date: datetime.datetime = Field(sa_column=Column('order_date', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    due_date: Optional[datetime.datetime] = Field(default=None, sa_column=Column('due_date', DateTime(True)))
    notes: Optional[str] = Field(default=None, sa_column=Column('notes', Text))

    customer: Optional['Customers'] = Relationship(back_populates='sales_orders')
    production_orders: list['ProductionOrders'] = Relationship(back_populates='sales_order')
    sales_order_items: list['SalesOrderItems'] = Relationship(back_populates='sales_order')


class Users(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['roles.id'], name='users_role_id_fkey'),
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    email: str = Field(sa_column=Column('email', String(254), nullable=False))
    full_name: str = Field(sa_column=Column('full_name', String(120), nullable=False))
    hashed_password: str = Field(sa_column=Column('hashed_password', String(255), nullable=False))
    role_id: int = Field(sa_column=Column('role_id', Integer, nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    is_active: Optional[bool] = Field(default=None, sa_column=Column('is_active', Boolean, server_default=text('true')))

    role: Optional['Roles'] = Relationship(back_populates='users')


class BomItems(SQLModel, table=True):
    __tablename__: str = 'bom_items'
    __table_args__ = (
        CheckConstraint('quantity > 0::numeric', name='bom_items_quantity_check'),
        ForeignKeyConstraint(['bom_id'], ['boms.id'], name='bom_items_bom_id_fkey'),
        ForeignKeyConstraint(['component_product_id'], ['products.id'], name='bom_items_component_product_id_fkey'),
        PrimaryKeyConstraint('id', name='bom_items_pkey'),
        UniqueConstraint('bom_id', 'component_product_id', name='bom_items_bom_id_component_product_id_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    bom_id: int = Field(sa_column=Column('bom_id', Integer, nullable=False))
    component_product_id: int = Field(sa_column=Column('component_product_id', Integer, nullable=False))
    quantity: decimal.Decimal = Field(sa_column=Column('quantity', Numeric, nullable=False))
    scrap_factor: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('scrap_factor', Numeric, server_default=text('0')))

    bom: Optional['Boms'] = Relationship(back_populates='bom_items')
    component_product: Optional['Products'] = Relationship(back_populates='bom_items')


class ProductionOrders(SQLModel, table=True):
    __tablename__: str = 'production_orders'
    __table_args__ = (
        ForeignKeyConstraint(['bom_id'], ['boms.id'], name='production_orders_bom_id_fkey'),
        ForeignKeyConstraint(['product_id'], ['products.id'], name='production_orders_product_id_fkey'),
        ForeignKeyConstraint(['routing_id'], ['routings.id'], name='production_orders_routing_id_fkey'),
        ForeignKeyConstraint(['sales_order_id'], ['sales_orders.id'], name='production_orders_sales_order_id_fkey'),
        PrimaryKeyConstraint('id', name='production_orders_pkey'),
        UniqueConstraint('po_number', name='production_orders_po_number_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    po_number: str = Field(sa_column=Column('po_number', String(32), nullable=False))
    status: str = Field(sa_column=Column('status', PgEnum('PLANNED', 'RELEASED', 'IN_PROCESS', 'COMPLETED', 'CANCELLED', name='prod_order_status_enum'), nullable=False))
    product_id: int = Field(sa_column=Column('product_id', Integer, nullable=False))
    quantity: decimal.Decimal = Field(sa_column=Column('quantity', Numeric, nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    sales_order_id: Optional[int] = Field(default=None, sa_column=Column('sales_order_id', Integer))
    bom_id: Optional[int] = Field(default=None, sa_column=Column('bom_id', Integer))
    routing_id: Optional[int] = Field(default=None, sa_column=Column('routing_id', Integer))
    due_date: Optional[datetime.datetime] = Field(default=None, sa_column=Column('due_date', DateTime(True)))
    started_at: Optional[datetime.datetime] = Field(default=None, sa_column=Column('started_at', DateTime(True)))
    completed_at: Optional[datetime.datetime] = Field(default=None, sa_column=Column('completed_at', DateTime(True)))

    bom: Optional['Boms'] = Relationship(back_populates='production_orders')
    product: Optional['Products'] = Relationship(back_populates='production_orders')
    routing: Optional['Routings'] = Relationship(back_populates='production_orders')
    sales_order: Optional['SalesOrders'] = Relationship(back_populates='production_orders')
    production_operations: list['ProductionOperations'] = Relationship(back_populates='production_order')


class RoutingOperations(SQLModel, table=True):
    __tablename__: str = 'routing_operations'
    __table_args__ = (
        CheckConstraint('sequence >= 10', name='routing_operations_sequence_check'),
        ForeignKeyConstraint(['routing_id'], ['routings.id'], name='routing_operations_routing_id_fkey'),
        ForeignKeyConstraint(['work_center_id'], ['work_centers.id'], name='routing_operations_work_center_id_fkey'),
        PrimaryKeyConstraint('id', name='routing_operations_pkey'),
        UniqueConstraint('routing_id', 'sequence', name='routing_operations_routing_id_sequence_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    routing_id: int = Field(sa_column=Column('routing_id', Integer, nullable=False))
    work_center_id: int = Field(sa_column=Column('work_center_id', Integer, nullable=False))
    sequence: int = Field(sa_column=Column('sequence', Integer, nullable=False))
    standard_time_minutes: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('standard_time_minutes', Numeric, server_default=text('0')))
    setup_time_minutes: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('setup_time_minutes', Numeric, server_default=text('0')))
    move_time_minutes: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('move_time_minutes', Numeric, server_default=text('0')))

    routing: Optional['Routings'] = Relationship(back_populates='routing_operations')
    work_center: Optional['WorkCenters'] = Relationship(back_populates='routing_operations')
    production_operations: list['ProductionOperations'] = Relationship(back_populates='routing_operation')


class SalesOrderItems(SQLModel, table=True):
    __tablename__: str = 'sales_order_items'
    __table_args__ = (
        CheckConstraint('quantity > 0::numeric', name='sales_order_items_quantity_check'),
        ForeignKeyConstraint(['bom_id'], ['boms.id'], name='sales_order_items_bom_id_fkey'),
        ForeignKeyConstraint(['product_id'], ['products.id'], name='sales_order_items_product_id_fkey'),
        ForeignKeyConstraint(['routing_id'], ['routings.id'], name='sales_order_items_routing_id_fkey'),
        ForeignKeyConstraint(['sales_order_id'], ['sales_orders.id'], name='sales_order_items_sales_order_id_fkey'),
        PrimaryKeyConstraint('id', name='sales_order_items_pkey'),
        UniqueConstraint('sales_order_id', 'line_no', name='sales_order_items_sales_order_id_line_no_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    sales_order_id: int = Field(sa_column=Column('sales_order_id', Integer, nullable=False))
    line_no: int = Field(sa_column=Column('line_no', Integer, nullable=False))
    product_id: int = Field(sa_column=Column('product_id', Integer, nullable=False))
    quantity: decimal.Decimal = Field(sa_column=Column('quantity', Numeric, nullable=False))
    unit_price: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('unit_price', Numeric, server_default=text('0')))
    bom_id: Optional[int] = Field(default=None, sa_column=Column('bom_id', Integer))
    routing_id: Optional[int] = Field(default=None, sa_column=Column('routing_id', Integer))

    bom: Optional['Boms'] = Relationship(back_populates='sales_order_items')
    product: Optional['Products'] = Relationship(back_populates='sales_order_items')
    routing: Optional['Routings'] = Relationship(back_populates='sales_order_items')
    sales_order: Optional['SalesOrders'] = Relationship(back_populates='sales_order_items')


class ProductionOperations(SQLModel, table=True):
    __tablename__: str = 'production_operations'
    __table_args__ = (
        ForeignKeyConstraint(['production_order_id'], ['production_orders.id'], name='production_operations_production_order_id_fkey'),
        ForeignKeyConstraint(['routing_operation_id'], ['routing_operations.id'], name='production_operations_routing_operation_id_fkey'),
        PrimaryKeyConstraint('id', name='production_operations_pkey'),
        UniqueConstraint('production_order_id', 'routing_operation_id', name='production_operations_production_order_id_routing_operation_key')
    )

    id: int = Field(sa_column=Column('id', Integer, primary_key=True))
    production_order_id: int = Field(sa_column=Column('production_order_id', Integer, nullable=False))
    routing_operation_id: int = Field(sa_column=Column('routing_operation_id', Integer, nullable=False))
    status: str = Field(sa_column=Column('status', PgEnum('PENDING', 'READY', 'STARTED', 'PAUSED', 'COMPLETED', 'BLOCKED', name='operation_status_enum'), nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    started_at: Optional[datetime.datetime] = Field(default=None, sa_column=Column('started_at', DateTime(True)))
    finished_at: Optional[datetime.datetime] = Field(default=None, sa_column=Column('finished_at', DateTime(True)))
    actual_time_minutes: Optional[decimal.Decimal] = Field(default=None, sa_column=Column('actual_time_minutes', Numeric))

    production_order: Optional['ProductionOrders'] = Relationship(back_populates='production_operations')
    routing_operation: Optional['RoutingOperations'] = Relationship(back_populates='production_operations')

metadata = SQLModel.metadata