# Repository Layer Guide

## Overview

The repository layer provides primitive CRUD operations for all entities in the MTO system. This layer focuses purely on database access and does not contain business logic. Business logic should be implemented in the service layer, which will use these primitive operations.

## Structure

All repository modules are located in `app/crud/repositories/` and follow a consistent pattern. They are re-exported through `app/crud/__init__.py` for convenient access.

## Created Repository Modules

### 1. **customers.py** - Customer Management
- `create_customer(db, data)` - Create new customer
- `get_customer_by_id(db, customer_id)` - Retrieve customer by ID
- `list_customers(db, skip=0, limit=10)` - List customers with pagination
- `update_customer(db, customer_id, data)` - Update customer
- `delete_customer(db, customer_id)` - Delete customer

### 2. **products.py** - Product Management
- `create_product(db, data)` - Create new product
- `get_product_by_id(db, product_id)` - Retrieve product by ID
- `list_products(db, skip=0, limit=10)` - List products with pagination
- `update_product(db, product_id, data)` - Update product
- `delete_product(db, product_id)` - Delete product

### 3. **orders.py** - Order Management
- `create_order(db, data)` - Create new order
- `get_order_by_id(db, order_id)` - Retrieve order by ID
- `list_orders(db, skip=0, limit=10)` - List orders with pagination
- `update_order(db, order_id, data)` - Update order
- `delete_order(db, order_id)` - Delete order

### 4. **order_items.py** - Order Item Management
- `create_order_item(db, data)` - Create new order item
- `get_order_item_by_id(db, item_id)` - Retrieve order item by ID
- `list_order_items(db, skip=0, limit=10)` - List order items with pagination
- `update_order_item(db, item_id, data)` - Update order item
- `delete_order_item(db, item_id)` - Delete order item

### 5. **planned_orders.py** - Planned Order Management
- `create_planned_order(db, data)` - Create new planned order
- `get_planned_order_by_id(db, planned_id)` - Retrieve planned order by ID
- `list_planned_orders(db, skip=0, limit=10)` - List planned orders with pagination
- `update_planned_order(db, planned_id, data)` - Update planned order
- `delete_planned_order(db, planned_id)` - Delete planned order

### 6. **work_orders.py** - Work Order Management
- `create_work_order(db, data)` - Create new work order
- `get_work_order_by_id(db, work_id)` - Retrieve work order by ID
- `list_work_orders(db, skip=0, limit=10)` - List work orders with pagination
- `update_work_order(db, work_id, data)` - Update work order
- `delete_work_order(db, work_id)` - Delete work order

### 7. **components.py** - Component Management
- `create_component(db, data)` - Create new component
- `get_component_by_id(db, component_id)` - Retrieve component by ID
- `list_components(db, skip=0, limit=10)` - List components with pagination
- `update_component(db, component_id, data)` - Update component
- `delete_component(db, component_id)` - Delete component

### 8. **component_usages.py** - Component Usage Management
- `create_component_usage(db, data)` - Create new component usage record
- `get_component_usage_by_id(db, usage_id)` - Retrieve component usage by ID
- `list_component_usages(db, skip=0, limit=10)` - List component usages with pagination
- `update_component_usage(db, usage_id, data)` - Update component usage
- `delete_component_usage(db, usage_id)` - Delete component usage

### 9. **deliveries_repo.py** - Delivery Management
- `create_delivery(db, data)` - Create new delivery
- `get_delivery_by_id(db, delivery_id)` - Retrieve delivery by ID
- `list_deliveries(db, skip=0, limit=10)` - List deliveries with pagination
- `update_delivery(db, delivery_id, data)` - Update delivery
- `delete_delivery(db, delivery_id)` - Delete delivery

### 10. **invoices.py** - Invoice Management
- `create_invoice(db, data)` - Create new invoice
- `get_invoice_by_id(db, invoice_id)` - Retrieve invoice by ID
- `list_invoices(db, skip=0, limit=10)` - List invoices with pagination
- `update_invoice(db, invoice_id, data)` - Update invoice
- `delete_invoice(db, invoice_id)` - Delete invoice

### 11. **order_component_usage.py** - View Accessor (Read-Only)
- `list_order_component_usage(db, order_id=None)` - Query aggregated component usage per order from view

## Usage Examples

### Creating a Customer
```python
from sqlalchemy.orm import Session
from app.crud import create_customer

def some_service_function(db: Session):
    customer_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "address": "123 Main St"
    }
    customer = create_customer(db, customer_data)
    return customer
```

### Updating an Order
```python
from app.crud import get_order_by_id, update_order
from app.models import OrderStatus

def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    order = get_order_by_id(db, order_id)
    if not order:
        return None
    
    updated_order = update_order(db, order_id, {"status": new_status})
    return updated_order
```

### Listing Products with Pagination
```python
from app.crud import list_products

def get_products_page(db: Session, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    products = list_products(db, skip=skip, limit=page_size)
    return products
```

### Querying Component Usage View
```python
from app.crud import list_order_component_usage

def get_component_usage_for_order(db: Session, order_id: int):
    # Get aggregated component usage for a specific order
    usage = list_order_component_usage(db, order_id=order_id)
    return usage
```

## Design Principles

### 1. **Primitive Operations Only**
- Each function performs a single database operation
- No business logic, validations, or complex workflows
- Service layer will orchestrate these operations for business logic

### 2. **Consistent Interface**
- All functions accept `db: Session` as first parameter
- Create functions accept `data: dict`
- Update functions accept `data: dict` with only fields to update
- Get functions return `Optional[Model]` (None if not found)
- List functions support pagination via `skip` and `limit`
- Delete functions return `bool` (True if deleted, False if not found)

### 3. **Error Handling**
- Repository layer returns `None` for not-found cases
- Database integrity errors (FK violations, unique constraints) bubble up
- Service layer should handle these exceptions and apply business logic

### 4. **Type Hints**
- All functions include proper type hints for parameters and return values
- Imports `Optional`, `List` from `typing` module

### 5. **Documentation**
- Every function has a docstring with Args and Returns sections
- Module-level docstrings explain the purpose

## Next Steps: Service Layer

The service layer will:
1. Use these repository functions to implement business logic
2. Handle validations (e.g., check if customer exists before creating order)
3. Implement workflows (e.g., Order → PlannedOrder → WorkOrder flow)
4. Handle transactions spanning multiple entities
5. Apply business rules and constraints
6. Return appropriate errors with context

Example service layer function:
```python
from app.crud import (
    create_order, create_order_item,
    get_customer_by_id, get_product_by_id
)
from app.models import OrderStatus

def create_order_with_items(
    db: Session,
    customer_id: int,
    items: List[dict]
) -> Order:
    # Validate customer exists
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise ValueError("Customer not found")
    
    # Create order
    order_data = {
        "customer_id": customer_id,
        "status": OrderStatus.NEW
    }
    order = create_order(db, order_data)
    
    # Create order items
    for item_data in items:
        product = get_product_by_id(db, item_data["product_id"])
        if not product:
            raise ValueError(f"Product {item_data['product_id']} not found")
        
        order_item_data = {
            "order_id": order.id,
            "product_id": product.id,
            "quantity": item_data["quantity"],
            "unit_price": product.price
        }
        create_order_item(db, order_item_data)
    
    return order
```

## Import Path

All functions are exported from `app.crud` (re-exported from `app.crud.repositories`):
```python
from app.crud import (
    create_customer, get_customer_by_id, list_customers,
    create_product, get_product_by_id,
    create_order, get_order_by_id,
    # ... etc
)

# Or import directly from repositories:
from app.crud.repositories import create_customer, get_customer_by_id
```

## Testing

When writing tests for the repository layer:
1. Use a test database or in-memory SQLite
2. Test each CRUD operation independently
3. Test edge cases (not found, duplicates, etc.)
4. Ensure transactions are properly rolled back in tests

Example test:
```python
def test_create_and_get_customer(db: Session):
    # Create
    data = {"name": "Test Customer", "email": "test@example.com"}
    customer = create_customer(db, data)
    assert customer.id is not None
    
    # Get
    fetched = get_customer_by_id(db, customer.id)
    assert fetched is not None
    assert fetched.name == "Test Customer"
    
    # Not found
    not_found = get_customer_by_id(db, 99999)
    assert not_found is None
```
