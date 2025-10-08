# 🧾 **PRD / RFC: Service Layer Implementation for Mapúa University MTO Backend**

---

## 1. Background

The **Mapúa University Bookstore** backend supports a Make-to-Order (MTO) flow where production starts only after a confirmed customer order.
This flow mirrors a simplified SAP PP/SD integration:

1. **Customer places Sales Order** via the e-commerce frontend.
2. **Production Manager** triggers manufacturing (via Production Order).
3. **Delivery Team** fulfills the completed goods.
4. **Billing Staff** issues invoices post-delivery.

The backend must manage this process with consistency, atomicity, and clear transitions between order states.

The **Service Layer** coordinates all these steps, sitting above the repository layer (CRUD) and below the router layer (API).
It contains **business rules**, **cross-entity transactions**, and **status progression logic**.

---

## 2. Purpose and Goals

### 🎯 Goal

Design and implement a **Service Layer** that encapsulates all core business logic for the MTO lifecycle, enabling:

* Multi-entity operations (e.g., creating a SalesOrder and its items in one transaction)
* Controlled workflow transitions between order stages
* Data consistency across `SalesOrder`, `ProductionOrder`, `Delivery`, and `Billing`

### 🧩 Key Objectives

| Objective                        | Description                                                             |
| -------------------------------- | ----------------------------------------------------------------------- |
| **Workflow Management**          | Implement the full MTO order flow with valid state transitions.         |
| **Atomic Transactions**          | Guarantee database integrity across repositories using shared sessions. |
| **Error Handling**               | Centralize validation and error propagation from repositories.          |
| **Business Logic Encapsulation** | Keep routers simple; move decision-making here.                         |
| **Extensibility**                | Allow adding workflows like returns, cancellations, or reporting later. |

---

## 3. Scope

### ✅ In Scope

* Business operations involving multiple repositories:

  * Sales order creation with items
  * Production start and completion
  * Delivery creation and fulfillment
  * Billing generation
* Validation of entity state before transition
* High-level orchestration of MTO flow

### ❌ Out of Scope

* Primitive CRUD (already handled by repositories)
* Request/response models or HTTP-level handling (belongs to routers)
* UI- or dashboard-related logic

---

## 4. Architectural Overview

### 🔧 Layer Stack

```
Routers (FastAPI endpoints)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (CRUD and data access)
    ↓
Database (SQLite / SQLModel)
```

### 🔁 MTO Flow Overview

```text
Sales Order (Created)
    ↓
Production Order (Planned → In Progress → Completed)
    ↓
Delivery (Pending → Delivered)
    ↓
Billing (Generated)
```

Each arrow corresponds to a service-layer process.

---

## 5. Design Principles

| Principle                           | Description                                                                         |
| ----------------------------------- | ----------------------------------------------------------------------------------- |
| **Single Transaction per Workflow** | Each business operation (e.g., order creation) commits atomically.                  |
| **Validation Before Mutation**      | Ensure entities exist and are in valid states before updates.                       |
| **Layered Dependency**              | Services depend only on repositories, never directly on SQLModel.                   |
| **Deterministic State Transitions** | Orders must move through allowed status states only.                                |
| **Reusability and Testability**     | Each service function can be tested independently using mock repos or in-memory DB. |

---

## 6. Service Layer Components

The service layer will consist of five modules:

```
app/services/
├── order_service.py
├── production_service.py
├── delivery_service.py
├── billing_service.py
└── product_service.py
```

Each module implements use-case-driven functions that coordinate one or more repositories.

---

## 7. Service Layer Functional Design

Below are **all required service functions**, grouped by business area.
Each entry details:

* **Purpose**
* **Repositories used**
* **Business rules and validations**

---

### 🧾 **Order Service (`order_service.py`)**

Handles creation and management of sales orders and their line items.

#### 1. `create_order_with_items(session, customer_id, items)`

**Purpose:** Create a sales order and corresponding sales order items in one atomic transaction.
**Repositories Used:** `ProductRepository`, `SalesOrderRepository`, `SalesOrderItemRepository`
**Business Logic:**

* Validate all product IDs exist.
* Calculate `subtotal` per item and total amount.
* Insert a new `SalesOrder` with `status="Created"`.
* Insert all `SalesOrderItem` records.
* Commit all together.
* Return the created order.

#### 2. `get_order_details(session, order_id)`

**Purpose:** Fetch full details of an order and its related entities.
**Repositories Used:** All (SalesOrder, SalesOrderItem, ProductionOrder, Delivery, Billing)
**Business Logic:**

* Retrieve order and all relationships.
* Return a composite structure suitable for order tracking UI.

#### 3. `update_order_status(session, order_id, status)`

**Purpose:** Move the order along the MTO flow stages.
**Repositories Used:** `SalesOrderRepository`
**Business Logic:**

* Only allow valid transitions:

  * Created → In Production
  * In Production → Ready for Delivery
  * Ready for Delivery → Billed
* Raise error for invalid transitions.

#### 4. `delete_order(session, order_id)`

**Purpose:** Cascade delete order and its items.
**Repositories Used:** `SalesOrderRepository`, `SalesOrderItemRepository`

---

### ⚙️ **Production Service (`production_service.py`)**

Manages creation and tracking of production orders tied to sales orders.

#### 1. `start_production_for_order(session, sales_order_id)`

**Purpose:** Trigger a production order for a sales order.
**Repositories Used:** `SalesOrderRepository`, `ProductionOrderRepository`
**Business Logic:**

* Validate that the sales order exists and status = “Created”.
* Create a `ProductionOrder` with `status="Planned"`.
* Update sales order → `status="In Production"`.

#### 2. `mark_production_in_progress(session, production_id)`

**Purpose:** Move production to active state.
**Repositories Used:** `ProductionOrderRepository`
**Business Logic:**

* Update status → “In Progress”.
* Log timestamp (`start_date` = now).

#### 3. `mark_production_complete(session, production_id)`

**Purpose:** Finalize production and update sales order.
**Repositories Used:** `ProductionOrderRepository`, `SalesOrderRepository`
**Business Logic:**

* Validate production exists and `status="In Progress"`.
* Update production → `status="Completed"`, set `end_date`.
* Update linked sales order → `status="Ready for Delivery"`.

---

### 🚚 **Delivery Service (`delivery_service.py`)**

Coordinates delivery records and their link to sales orders.

#### 1. `create_delivery_for_order(session, sales_order_id, delivery_date)`

**Purpose:** Create a delivery record for completed order.
**Repositories Used:** `DeliveryRepository`, `SalesOrderRepository`
**Business Logic:**

* Validate that the sales order is `status="Ready for Delivery"`.
* Create delivery with `status="Pending"`.
* Return delivery record.

#### 2. `mark_delivery_done(session, delivery_id)`

**Purpose:** Mark a delivery as complete and update order.
**Repositories Used:** `DeliveryRepository`, `SalesOrderRepository`
**Business Logic:**

* Validate delivery exists and `status="Pending"`.
* Update delivery → `status="Delivered"`, `delivery_date=now()`.
* Update linked sales order → `status="Delivered"`.

---

### 💵 **Billing Service (`billing_service.py`)**

Handles invoice generation and billing records.

#### 1. `generate_billing_for_order(session, sales_order_id)`

**Purpose:** Generate invoice after delivery completion.
**Repositories Used:** `BillingRepository`, `SalesOrderRepository`
**Business Logic:**

* Validate sales order status = “Delivered”.
* Generate `invoice_number` pattern: `INV-{YYYY}-{random4}`.
* Compute total from sales order.
* Create billing record with `billed_date=now()`.
* Update order → `status="Billed"`.

#### 2. `get_billing_for_order(session, sales_order_id)`

**Purpose:** Retrieve billing record for display.
**Repositories Used:** `BillingRepository`

---

### 🏷️ **Product Service (`product_service.py`)**

Provides higher-level operations for managing products and stock (optional enhancements).

#### 1. `create_product_with_stock(session, product_data, stock_qty)`

**Purpose:** Create product and optionally seed stock.
**Repositories Used:** `ProductRepository`

#### 2. `restock_product(session, product_id, quantity)`

**Purpose:** Update stock levels.
**Repositories Used:** `ProductRepository`
**Business Logic:** Add to existing `stock_qty`, never go negative.

---

## 8. Transaction Management

All service-layer write operations should use **a single session** shared across repository calls.

Example:

```python
with Session(engine) as session:
    try:
        order = order_service.create_order_with_items(session, 1, items)
    except Exception:
        session.rollback()
        raise
```

* Repositories themselves **do not close the session**.
* The **service function** owns transaction boundaries.

---

## 9. Error Handling

| Error Type               | Example Cause                     | Handling Strategy                 |
| ------------------------ | --------------------------------- | --------------------------------- |
| `EntityNotFoundError`    | Missing product/order             | Raise and catch at router → 404   |
| `InvalidTransitionError` | Skipping from Created → Delivered | Raise custom business error → 400 |
| `IntegrityError`         | Duplicate keys                    | Rollback transaction, rethrow     |
| Generic Exception        | Any unexpected issue              | Rollback and log                  |

Custom errors (in `exceptions.py`):

```python
class InvalidTransitionError(Exception): ...
class EntityNotFoundError(Exception): ...
```

---

## 10. Logging & Auditing

Every major transition (production start, delivery, billing) should log an info-level message.
This aids in tracing the flow for audit or debugging.

Example:

```python
logger.info(f"Order {order_id} moved to In Production by ProductionService")
```

---

## 11. Testing Plan

| Test Type            | Example                                       | Expected Outcome                    |
| -------------------- | --------------------------------------------- | ----------------------------------- |
| **Unit**             | Create order with valid products              | Returns order with correct totals   |
| **Unit**             | Attempt production start on nonexistent order | Raises EntityNotFoundError          |
| **Integration**      | Complete full flow (Order → Billing)          | Sales order final status = “Billed” |
| **State Transition** | Invalid jump (Created → Billed)               | Raises InvalidTransitionError       |

---

## 12. Deliverables

| File                             | Description                           |
| -------------------------------- | ------------------------------------- |
| `services/order_service.py`      | Sales order orchestration logic       |
| `services/production_service.py` | Production management logic           |
| `services/delivery_service.py`   | Delivery handling logic               |
| `services/billing_service.py`    | Billing and invoicing logic           |
| `services/product_service.py`    | Product-related business logic        |
| `exceptions.py`                  | Shared business exception definitions |
| `tests/test_services.py`         | Unit and integration tests            |

---

## 13. Acceptance Criteria

* [ ] All service functions encapsulate **multi-repository** logic.
* [ ] All order state transitions validated.
* [ ] Database consistency verified through end-to-end tests.
* [ ] Service layer functions do not directly use SQLModel — only repository calls.
* [ ] All functions return domain entities or meaningful results (never raw ORM queries).
* [ ] End-to-end workflow results in correct final statuses:

  ```
  Created → In Production → Ready for Delivery → Delivered → Billed
  ```

---

## 14. Future Considerations

* **Async support** (migrate repositories to async SQLModel).
* **Event-based notifications** (emit domain events like “OrderReadyForDelivery”).
* **Inventory tracking** (deduct stock on order creation).
* **Audit log table** for all status transitions.
* **Refund / cancellation workflow**.

---

✅ **Summary**

This PRD defines a service layer that:

* Implements the full **MTO business flow** end-to-end,
* Encapsulates all multi-entity business logic,
* Enforces correct state transitions and consistency,
* Lays a solid foundation for scaling into a production-ready ERP-like flow.
