"""API endpoint integration tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from app.database import get_session
from app.main import app
# Import all models to ensure they are registered with SQLModel metadata
from app import models


@pytest.fixture(name="client")
def client_fixture():
    """Provide a test client with a fresh in-memory database."""

    # Create in-memory database for testing
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    # Override the database session for testing
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    # Clean up
    SQLModel.metadata.drop_all(engine)
    app.dependency_overrides.clear()


def test_list_orders_empty(client: TestClient) -> None:
    """Test listing orders when none exist."""

    response = client.get("/api/orders")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] == []


def test_dashboard_summary(client: TestClient) -> None:
    """Test dashboard summary endpoint."""

    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "total_orders" in data["data"]
    assert "in_production" in data["data"]
    assert "ready_for_delivery" in data["data"]
    assert "billed" in data["data"]
    assert "top_products" in data["data"]
    assert "recent_orders" in data["data"]


def test_list_customers_empty(client: TestClient) -> None:
    """Test listing customers when none exist."""

    response = client.get("/api/customers")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] == []


def test_list_products_empty(client: TestClient) -> None:
    """Test listing products when none exist."""

    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] == []


def test_create_order_missing_customer(client: TestClient) -> None:
    """Test creating an order with non-existent customer."""

    response = client.post(
        "/api/orders",
        json={
            "customer_id": 999,
            "items": [
                {"product_id": 1, "quantity": 1},
            ],
        },
    )
    assert response.status_code == 400


def test_create_order_missing_product(client: TestClient) -> None:
    """Test creating an order with non-existent product."""

    response = client.post(
        "/api/orders",
        json={
            "customer_id": 1,
            "items": [
                {"product_id": 999, "quantity": 1},
            ],
        },
    )
    assert response.status_code == 400
