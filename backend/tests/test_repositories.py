"""Unit tests for repository layer operations."""

from __future__ import annotations

import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.models import (
    Billing,
    Customer,
    Delivery,
    DeliveryStatus,
    Product,
    ProductionOrder,
    ProductionOrderStatus,
    SalesOrder,
    SalesOrderItem,
    SalesOrderStatus,
)
from app.repositories.billing_repository import BillingRepository
from app.repositories.base_repository import BaseRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.exceptions import EntityNotFoundError
from app.repositories.product_repository import ProductRepository
from app.repositories.production_order_repository import ProductionOrderRepository
from app.repositories.sales_order_item_repository import SalesOrderItemRepository
from app.repositories.sales_order_repository import SalesOrderRepository


@pytest.fixture(name="session")
def session_fixture() -> Session:
    """Provide a transactional in-memory database session for testing."""
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def test_product_repository_crud(session: Session) -> None:
    repo = ProductRepository()
    created = repo.create(
        session,
        {"name": "Hoodie", "description": "Red hoodie", "price": 599.0, "stock_qty": 25},
    )
    assert created.id is not None

    found_by_name = repo.find_by_name(session, "Hoodie")
    assert found_by_name is not None
    assert found_by_name.id == created.id

    updated = repo.update(session, created.id, {"price": 649.0})
    assert updated.price == 649.0

    listed = repo.list(session)
    assert len(listed) == 1

    deleted = repo.delete(session, created.id)
    assert deleted is True
    assert repo.get(session, created.id) is None


def test_customer_repository_lookup(session: Session) -> None:
    repo = CustomerRepository()
    customer = repo.create(
        session,
        {"name": "Jane Doe", "email": "jane@example.com", "role": "student"},
    )
    fetched = repo.find_by_email(session, "jane@example.com")
    assert fetched is not None
    assert fetched.id == customer.id


def test_sales_order_repository_queries(session: Session) -> None:
    customer = CustomerRepository().create(
        session,
        {"name": "Acme", "email": "acme@example.com", "role": "department"},
    )
    repo = SalesOrderRepository()
    order = repo.create(
        session,
        {
            "customer_id": customer.id,
            "total_amount": 1500.0,
            "status": SalesOrderStatus.created,
        },
    )
    orders_for_customer = repo.list_by_customer(session, customer.id)
    assert len(orders_for_customer) == 1

    repo.update_status(session, order.id, SalesOrderStatus.in_production)
    refreshed = repo.get_or_raise(session, order.id)
    assert refreshed.status == SalesOrderStatus.in_production

    in_production_orders = repo.list_by_status(session, SalesOrderStatus.in_production)
    assert len(in_production_orders) == 1


def test_sales_order_item_repository(session: Session) -> None:
    product = ProductRepository().create(
        session,
        {"name": "Shirt", "description": "White shirt", "price": 299.0, "stock_qty": 50},
    )
    customer = CustomerRepository().create(
        session,
        {"name": "John", "email": "john@example.com", "role": "student"},
    )
    order = SalesOrderRepository().create(
        session,
        {
            "customer_id": customer.id,
            "total_amount": 299.0,
            "status": SalesOrderStatus.created,
        },
    )
    item_repo = SalesOrderItemRepository()
    item = item_repo.create(
        session,
        {
            "sales_order_id": order.id,
            "product_id": product.id,
            "quantity": 2,
            "subtotal": 598.0,
        },
    )
    items_for_order = item_repo.list_by_order(session, order.id)
    assert len(items_for_order) == 1
    assert items_for_order[0].id == item.id


def test_production_order_repository(session: Session) -> None:
    customer = CustomerRepository().create(
        session,
        {"name": "Ops", "email": "ops@example.com", "role": "department"},
    )
    order = SalesOrderRepository().create(
        session,
        {
            "customer_id": customer.id,
            "total_amount": 750.0,
            "status": SalesOrderStatus.created,
        },
    )
    repo = ProductionOrderRepository()
    prod = repo.create(
        session,
        {
            "sales_order_id": order.id,
            "status": ProductionOrderStatus.planned,
        },
    )
    by_status = repo.list_by_status(session, ProductionOrderStatus.planned)
    assert prod in by_status

    by_order = repo.list_by_sales_order(session, order.id)
    assert len(by_order) == 1


def test_delivery_repository(session: Session) -> None:
    customer = CustomerRepository().create(
        session,
        {"name": "Logistics", "email": "logistics@example.com", "role": "department"},
    )
    order = SalesOrderRepository().create(
        session,
        {
            "customer_id": customer.id,
            "total_amount": 500.0,
            "status": SalesOrderStatus.ready_for_delivery,
        },
    )
    repo = DeliveryRepository()
    delivery = repo.create(
        session,
        {
            "sales_order_id": order.id,
            "status": DeliveryStatus.pending,
        },
    )
    by_status = repo.list_by_status(session, DeliveryStatus.pending)
    assert delivery in by_status

    by_order = repo.list_by_sales_order(session, order.id)
    assert len(by_order) == 1


def test_billing_repository(session: Session) -> None:
    customer = CustomerRepository().create(
        session,
        {"name": "Finance", "email": "finance@example.com", "role": "department"},
    )
    order = SalesOrderRepository().create(
        session,
        {
            "customer_id": customer.id,
            "total_amount": 1800.0,
            "status": SalesOrderStatus.delivered,
        },
    )
    repo = BillingRepository()
    billing = repo.create(
        session,
        {
            "sales_order_id": order.id,
            "amount": 1800.0,
        },
    )
    fetched = repo.get_by_sales_order(session, order.id)
    assert fetched is not None
    assert fetched.id == billing.id


def test_entity_not_found_error(session: Session) -> None:
    repo: BaseRepository[Customer] = BaseRepository(Customer)
    with pytest.raises(EntityNotFoundError):
        repo.get_or_raise(session, 999)

    with pytest.raises(EntityNotFoundError):
        repo.delete(session, 999)
