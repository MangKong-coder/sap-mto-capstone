# 🧾 **PRD / RFC: Repository Layer Implementation for Mapúa University MTO Backend**

## 1. Background

Mapúa University’s Bookstore is expanding operations to handle **Make-to-Order (MTO)** production of university merchandise — such as hoodies, shirts, tote bags, and mugs.
Orders can originate from either:

* **Students/Faculty (retail)**, or
* **Departments (bulk orders)**.

The backend will manage the **complete order-to-cash process**:

1. Customer places a sales order.
2. Order triggers a production order.
3. Completed goods are delivered.
4. Billing is generated.

To keep the backend maintainable and scalable, it will follow a **clean layered architecture**, separating persistence from business logic.
This PRD covers the **Repository Layer**, which provides all *primitive data access operations* used by higher-level **Service Layer** processes.

---

## 2. Purpose and Goals

### 🎯 Goal

Design and implement a robust **Repository Layer** that:

* Encapsulates direct database operations for each entity.
* Provides consistent CRUD interfaces across models.
* Enables higher-level workflows (in the service layer) to compose these operations safely.
* Uses **SQLModel** with **SQLite** for simplicity and type safety.

### 🧩 Key Objectives

| Objective                  | Description                                                                                 |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| **Separation of Concerns** | Keep raw CRUD logic independent from business logic.                                        |
| **Reusability**            | Provide standard repository methods (create, get, update, delete) reusable across services. |
| **Consistency**            | Use uniform naming and error-handling patterns.                                             |
| **Extensibility**          | Allow switching databases (SQLite → Postgres) later without rewriting services.             |

---

## 3. Scope

### ✅ **In Scope**

* Repository classes/functions for each entity:

  * `Product`
  * `Customer`
  * `SalesOrder`
  * `SalesOrderItem`
  * `ProductionOrder`
  * `Delivery`
  * `Billing`
* Integration with **SQLModel** and shared session handling.
* Basic filtering (e.g., list by status or customer_id).
* Transaction safety for create/update/delete.
* Standardized error handling (e.g., `EntityNotFoundError`).

### ❌ **Out of Scope**

* Cross-entity or workflow logic (belongs to service layer).
* API routing or request/response validation.
* Business rules like totals, invoice generation, etc.

---

## 4. Architectural Overview

### 🏗️ System Layers Context

```
Frontend (Next.js Apps)
      ↓
FastAPI Routers → Service Layer → Repository Layer → Database (SQLite via SQLModel)
```

Each repository module maps **1:1** with a database table (SQLModel entity)
and provides basic CRUD primitives.

---

## 5. Data Entities (Schema Recap)

The repository layer will interact with these SQLModel classes:

* `Customer`
* `Product`
* `SalesOrder`
* `SalesOrderItem`
* `ProductionOrder`
* `Delivery`
* `Billing`

Each class has `id` as primary key and standard timestamps/relationships.

---

## 6. Design Principles

| Principle                            | Description                                                               |
| ------------------------------------ | ------------------------------------------------------------------------- |
| **Single Responsibility**            | Each repository manages only one model.                                   |
| **Session Injection**                | Database session passed from FastAPI dependency (`Depends(get_session)`). |
| **Composability**                    | Higher-level logic (services) composes multiple repositories.             |
| **Return Entities, not ORM Queries** | Each function returns typed SQLModel objects or lists.                    |
| **Soft Validation**                  | Repositories assume valid inputs; validation happens in service layer.    |

---

## 7. Repository Interface Design

### 7.1. Base Repository Pattern

Create a reusable abstract base class for consistency:

```python
from typing import Type, TypeVar, Generic, List, Optional
from sqlmodel import SQLModel, Session, select

T = TypeVar("T", bound=SQLModel)

class BaseRepository(Generic[T]):
    model: Type[T]

    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, session: Session, obj_data: dict) -> T:
        obj = self.model(**obj_data)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def get(self, session: Session, id: int) -> Optional[T]:
        return session.get(self.model, id)

    def list(self, session: Session) -> List[T]:
        return session.exec(select(self.model)).all()

    def update(self, session: Session, id: int, data: dict) -> Optional[T]:
        obj = session.get(self.model, id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, id: int) -> bool:
        obj = session.get(self.model, id)
        if not obj:
            return False
        session.delete(obj)
        session.commit()
        return True
```

This base will be subclassed by each specific repository.

---

### 7.2. Concrete Repositories

Each entity gets a dedicated repository that extends `BaseRepository`
and may define **custom query methods**.

#### 🏷️ `ProductRepository`

```python
class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)

    def find_by_name(self, session: Session, name: str) -> Optional[Product]:
        return session.exec(select(Product).where(Product.name == name)).first()
```

#### 👤 `CustomerRepository`

```python
class CustomerRepository(BaseRepository[Customer]):
    def __init__(self):
        super().__init__(Customer)
```

#### 📄 `SalesOrderRepository`

```python
class SalesOrderRepository(BaseRepository[SalesOrder]):
    def __init__(self):
        super().__init__(SalesOrder)

    def list_by_customer(self, session: Session, customer_id: int):
        return session.exec(select(SalesOrder).where(SalesOrder.customer_id == customer_id)).all()

    def update_status(self, session: Session, order_id: int, status: str):
        return self.update(session, order_id, {"status": status})
```

#### 🧾 `SalesOrderItemRepository`

```python
class SalesOrderItemRepository(BaseRepository[SalesOrderItem]):
    def __init__(self):
        super().__init__(SalesOrderItem)

    def list_by_order(self, session: Session, order_id: int):
        return session.exec(select(SalesOrderItem).where(SalesOrderItem.sales_order_id == order_id)).all()
```

#### ⚙️ `ProductionOrderRepository`

```python
class ProductionOrderRepository(BaseRepository[ProductionOrder]):
    def __init__(self):
        super().__init__(ProductionOrder)

    def list_by_status(self, session: Session, status: str):
        return session.exec(select(ProductionOrder).where(ProductionOrder.status == status)).all()
```

#### 🚚 `DeliveryRepository`

```python
class DeliveryRepository(BaseRepository[Delivery]):
    def __init__(self):
        super().__init__(Delivery)

    def list_by_status(self, session: Session, status: str):
        return session.exec(select(Delivery).where(Delivery.status == status)).all()
```

#### 💵 `BillingRepository`

```python
class BillingRepository(BaseRepository[Billing]):
    def __init__(self):
        super().__init__(Billing)

    def get_by_order(self, session: Session, sales_order_id: int):
        return session.exec(select(Billing).where(Billing.sales_order_id == sales_order_id)).first()
```

---

## 8. Folder and Module Structure

```
app/
└── repositories/
    ├── __init__.py
    ├── base_repository.py
    ├── product_repository.py
    ├── customer_repository.py
    ├── sales_order_repository.py
    ├── sales_order_item_repository.py
    ├── production_order_repository.py
    ├── delivery_repository.py
    └── billing_repository.py
```

---

## 9. Error Handling

Introduce a simple custom exception for missing entities:

```python
class EntityNotFoundError(Exception):
    def __init__(self, entity_name: str, entity_id: int):
        self.message = f"{entity_name} with id={entity_id} not found."
        super().__init__(self.message)
```

Repositories can raise this where applicable;
service layer will handle and translate into HTTP 404 responses.

---

## 10. Testing Plan

| Type                   | Description                                                             | Tool                                 |
| ---------------------- | ----------------------------------------------------------------------- | ------------------------------------ |
| **Unit Tests**         | Verify each CRUD method (create, get, update, delete) works as expected | `pytest`                             |
| **Integration Tests**  | Ensure repository methods interact with real SQLite file                | `pytest + testcontainers` (optional) |
| **Performance Checks** | Simple load test on list queries for larger datasets                    | Manual / Locust                      |

---

## 11. Example Usage in Service Layer

```python
def create_order_with_items(session, customer_id, items):
    total = 0
    for i in items:
        product = ProductRepository().get(session, i["product_id"])
        total += product.price * i["quantity"]

    order = SalesOrderRepository().create(session, {
        "customer_id": customer_id,
        "total_amount": total,
        "status": "Created"
    })

    for i in items:
        SalesOrderItemRepository().create(session, {
            "sales_order_id": order.id,
            "product_id": i["product_id"],
            "quantity": i["quantity"],
            "subtotal": product.price * i["quantity"]
        })

    return order
```

---

## 12. Deliverables

| Deliverable                  | Description                             |
| ---------------------------- | --------------------------------------- |
| `BaseRepository`             | Abstract base with shared CRUD logic    |
| `*_repository.py`            | One repository module per model         |
| `EntityNotFoundError`        | Shared exception class                  |
| `tests/test_repositories.py` | Unit tests for CRUD operations          |
| `README.md`                  | Short documentation of repository usage |

---

## 13. Acceptance Criteria

* [ ] Each repository supports full CRUD.
* [ ] Code passes unit tests using in-memory SQLite.
* [ ] All methods return model instances or lists.
* [ ] Common interface (create/get/list/update/delete) consistent across all entities.
* [ ] No direct SQL or cross-entity logic appears here.
* [ ] Service layer can fully depend on repository API without touching SQLModel directly.

---

## 14. Future Considerations

* Replace SQLite with PostgreSQL by swapping engine in `database.py`.
* Add pagination and sorting methods in repositories.
* Introduce async repository interface (for FastAPI async endpoints).
* Add caching layer (e.g., Redis) for frequent `list_*` queries.
* Implement soft-delete (archival) flags.

---

✅ **Summary**

This Repository Layer PRD defines:

* the **scope, purpose, and implementation plan** for entity-specific CRUD logic,
* ensures proper separation from the Service Layer,
* and lays the foundation for stable, testable backend workflows.