"""Unit tests for the service layer business workflows."""

from __future__ import annotations

from uuid import uuid4

import pytest
from sqlmodel import SQLModel, Session, create_engine

from app.models import (
    DeliveryStatus,
    ProductionOrderStatus,
    SalesOrderStatus,
)
from app.repositories.billing_repository import BillingRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.production_order_repository import ProductionOrderRepository
from app.repositories.sales_order_item_repository import SalesOrderItemRepository
from app.repositories.sales_order_repository import SalesOrderRepository
from app.services import (
    billing_service,
    delivery_service,
    order_service,
    product_service,
    production_service,
)
from app.services.exceptions import InvalidTransitionError


customer_repo = CustomerRepository()
product_repo = ProductRepository()
sales_order_repo = SalesOrderRepository()
sales_order_item_repo = SalesOrderItemRepository()
production_repo = ProductionOrderRepository()
delivery_repo = DeliveryRepository()
billing_repo = BillingRepository()


@pytest.fixture(name="session")
def session_fixture() -> Session:
    """Provide a transactional in-memory database session for service tests."""

    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def _create_customer(session: Session) -> int:
    customer = customer_repo.create(
        session,
        {
            "name": "Test Customer",
            "email": f"customer-{uuid4().hex}@example.com",
            "role": "student",
        },
    )
    return customer.id


def _create_product(session: Session, price: float = 100.0) -> int:
    product = product_repo.create(
        session,
        {
            "name": f"Hoodie {uuid4().hex[:6]}",
            "description": "Comfortable hoodie",
            "price": price,
            "stock_qty": 50,
        },
    )
    return product.id


def test_create_order_with_items_success(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session, price=250.0)

    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 2}],
    )

    assert order.status == SalesOrderStatus.created
    assert order.total_amount == pytest.approx(500.0)

    items = sales_order_item_repo.list_by_order(session, order.id)
    assert len(items) == 1
    assert items[0].quantity == 2


def test_create_order_with_items_invalid_quantity(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)

    with pytest.raises(ValueError):
        order_service.create_order_with_items(
            session,
            customer_id,
            [{"product_id": product_id, "quantity": 0}],
        )


def test_get_order_details_returns_related_entities(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 1}],
    )

    production = production_service.start_production_for_order(session, order.id)
    production_service.mark_production_in_progress(session, production.id)
    production_service.mark_production_complete(session, production.id)

    delivery = delivery_service.create_delivery_for_order(session, order.id)
    delivery_service.mark_delivery_done(session, delivery.id)

    billing_service.generate_billing_for_order(session, order.id)

    details = order_service.get_order_details(session, order.id)
    assert details["order"].id == order.id
    assert len(details["items"]) == 1
    assert len(details["production_orders"]) == 1
    assert len(details["deliveries"]) == 1
    assert details["billing"] is not None


def test_update_order_status_valid_transition(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 1}],
    )

    updated = order_service.update_order_status(
        session,
        order.id,
        SalesOrderStatus.in_production,
    )
    assert updated.status == SalesOrderStatus.in_production


def test_update_order_status_invalid_transition(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 1}],
    )

    with pytest.raises(InvalidTransitionError):
        order_service.update_order_status(
            session,
            order.id,
            SalesOrderStatus.delivered,
        )


def test_update_order_status_creates_delivery_entity(session: Session) -> None:
    """Test that transitioning to ready_for_delivery automatically creates a delivery."""
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 1}],
    )
    
    # Verify no delivery exists yet
    deliveries = delivery_repo.list_by_sales_order(session, order.id)
    assert len(deliveries) == 0
    
    # Transition through production
    order_service.update_order_status(session, order.id, SalesOrderStatus.in_production)
    
    # Transition to ready_for_delivery should create delivery
    order_service.update_order_status(session, order.id, SalesOrderStatus.ready_for_delivery)
    
    # Verify delivery was created
    deliveries = delivery_repo.list_by_sales_order(session, order.id)
    assert len(deliveries) == 1
    assert deliveries[0].status == DeliveryStatus.pending
    assert deliveries[0].sales_order_id == order.id


def test_update_order_status_creates_billing_entity(session: Session) -> None:
    """Test that transitioning to delivered automatically creates a billing."""
    customer_id = _create_customer(session)
    product_id = _create_product(session, price=150.0)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 2}],
    )
    
    # Verify no billing exists yet
    billing = billing_repo.get_by_sales_order(session, order.id)
    assert billing is None
    
    # Transition through statuses
    order_service.update_order_status(session, order.id, SalesOrderStatus.in_production)
    order_service.update_order_status(session, order.id, SalesOrderStatus.ready_for_delivery)
    
    # Transition to delivered should create billing
    order_service.update_order_status(session, order.id, SalesOrderStatus.delivered)
    
    # Verify billing was created
    billing = billing_repo.get_by_sales_order(session, order.id)
    assert billing is not None
    assert billing.amount == pytest.approx(300.0)
    assert billing.invoice_number == f"INV-{order.id:06d}"
    assert billing.sales_order_id == order.id


def test_delete_order_removes_items(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 3}],
    )

    deleted = order_service.delete_order(session, order.id)
    assert deleted is True
    assert sales_order_repo.get(session, order.id) is None
    assert sales_order_item_repo.list_by_order(session, order.id) == []


def test_start_production_for_order_invalid_status(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 1}],
    )

    production_service.start_production_for_order(session, order.id)

    with pytest.raises(InvalidTransitionError):
        production_service.start_production_for_order(session, order.id)


def test_mark_production_in_progress_flow(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 1}],
    )

    production = production_service.start_production_for_order(session, order.id)
    in_progress = production_service.mark_production_in_progress(session, production.id)
    assert in_progress.status == ProductionOrderStatus.in_progress
    assert in_progress.start_date is not None

    completed = production_service.mark_production_complete(session, production.id)
    assert completed.status == ProductionOrderStatus.completed

    order_refreshed = sales_order_repo.get_or_raise(session, order.id)
    assert order_refreshed.status == SalesOrderStatus.ready_for_delivery

    with pytest.raises(InvalidTransitionError):
        production_service.mark_production_complete(session, production.id)


def test_create_delivery_requires_ready_status(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 1}],
    )

    with pytest.raises(InvalidTransitionError):
        delivery_service.create_delivery_for_order(session, order.id)


def test_delivery_flow_updates_order(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 1}],
    )

    production = production_service.start_production_for_order(session, order.id)
    production_service.mark_production_in_progress(session, production.id)
    production_service.mark_production_complete(session, production.id)

    delivery = delivery_service.create_delivery_for_order(session, order.id)
    updated_delivery = delivery_service.mark_delivery_done(session, delivery.id)
    assert updated_delivery.status == DeliveryStatus.delivered
    assert updated_delivery.delivery_date is not None

    order_refreshed = sales_order_repo.get_or_raise(session, order.id)
    assert order_refreshed.status == SalesOrderStatus.delivered

    with pytest.raises(InvalidTransitionError):
        delivery_service.mark_delivery_done(session, delivery.id)


def test_generate_billing_requires_delivered_status(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 1}],
    )

    production = production_service.start_production_for_order(session, order.id)
    production_service.mark_production_in_progress(session, production.id)
    production_service.mark_production_complete(session, production.id)

    with pytest.raises(InvalidTransitionError):
        billing_service.generate_billing_for_order(session, order.id)


def test_generate_billing_idempotent(session: Session) -> None:
    customer_id = _create_customer(session)
    product_id = _create_product(session)
    order = order_service.create_order_with_items(
        session,
        customer_id,
        [{"product_id": product_id, "quantity": 1}],
    )

    production = production_service.start_production_for_order(session, order.id)
    production_service.mark_production_in_progress(session, production.id)
    production_service.mark_production_complete(session, production.id)

    delivery = delivery_service.create_delivery_for_order(session, order.id)
    delivery_service.mark_delivery_done(session, delivery.id)

    first = billing_service.generate_billing_for_order(session, order.id)
    second = billing_service.generate_billing_for_order(session, order.id)

    assert first.id == second.id
    assert first.invoice_number == second.invoice_number


def test_product_creation_and_restock(session: Session) -> None:
    product = product_service.create_product_with_stock(
        session,
        {
            "name": "Classic Tee",
            "description": "Comfort tee",
            "price": 199.0,
        },
        stock_qty=10,
    )
    assert product.stock_qty == 10

    updated = product_service.restock_product(session, product.id, 5)
    assert updated.stock_qty == 15

    with pytest.raises(ValueError):
        product_service.restock_product(session, product.id, 0)

    with pytest.raises(ValueError):
        product_service.create_product_with_stock(
            session,
            {
                "name": "Invalid Stock",
                "description": "Invalid",
                "price": 100.0,
            },
            stock_qty=-1,
        )
