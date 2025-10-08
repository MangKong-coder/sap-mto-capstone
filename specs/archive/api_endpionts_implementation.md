# 🧾 **PRD / RFC: API Endpoints Layer — Mapúa University MTO Backend**

---

## 1. Background

Mapúa University’s Bookstore is adopting a **Make-to-Order (MTO)** manufacturing flow for custom and bulk university merchandise.
The backend now has a completed **Repository Layer** (CRUD) and **Service Layer** (business orchestration).

The final phase is to expose these capabilities via a **RESTful API**, allowing two frontend applications to interact with the system:

1. 🛍️ **E-Commerce Frontend (Customer-Facing)**

   * Customers (students, faculty, or departments) browse products, place orders, and track their order statuses.
2. 🧭 **Fiori-Like Dashboard (Admin/Staff-Facing)**

   * Storefront staff, production managers, and billing clerks manage orders, production, deliveries, and billing operations.

This document specifies all required **API endpoints**, their **expected request/response structures**, and how they map to your existing **service layer** functions.

---

## 2. Purpose and Goals

### 🎯 **Goal**

Provide a stable and predictable REST API layer that:

* Exposes all MTO business workflows
* Provides consistent JSON responses
* Delegates logic to the service layer (no database logic inside routes)
* Supports optional filters (e.g., `status`, `search`)
* Omits pagination for simplicity — all list endpoints return complete datasets

---

## 3. Architectural Overview

```
Frontend (Next.js Apps)
        ↓
API Layer (FastAPI Routers)
        ↓
Service Layer (Business Logic)
        ↓
Repository Layer (CRUD)
        ↓
Database (SQLite via SQLModel)
```

Each router represents a domain module and contains:

* Route definitions
* Request/response schemas (Pydantic)
* Error handling and status codes

---

## 4. Design Principles

| Principle                  | Description                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------- |
| **RESTful and Consistent** | HTTP verbs reflect intent: GET (read), POST (create), PATCH (update), DELETE (remove) |
| **Service Delegation**     | All routes call service-layer functions; no direct ORM usage                          |
| **Atomicity & Validation** | Services ensure transaction consistency                                               |
| **Descriptive Responses**  | Standardized success/error payloads                                                   |
| **No Pagination**          | All list endpoints return complete sets (filtered when needed)                        |

---

## 5. Response and Error Standards

### ✅ Success Response

```json
{
  "success": true,
  "data": {...},
  "message": "Optional message"
}
```

### ❌ Error Response

```json
{
  "success": false,
  "error": "EntityNotFoundError",
  "message": "Sales order not found"
}
```

**Error to HTTP Status Mapping:**

| Error                    | Status |
| ------------------------ | ------ |
| `EntityNotFoundError`    | 404    |
| `InvalidTransitionError` | 400    |
| Generic                  | 500    |

---

## 6. Folder Structure

```
app/
└── routers/
    ├── orders.py
    ├── production_orders.py
    ├── deliveries.py
    ├── billings.py
    ├── products.py
    ├── customers.py
    └── dashboard.py
```

---

## 7. Endpoint Specifications

Each section lists routes, purpose, service layer mapping, and example payloads.

---

### 🧾 **Orders API (`/api/orders`)**

#### **GET /api/orders?status=**

* **Purpose:** Retrieve all sales orders, optionally filtered by status.
* **Service:** `order_service.get_customer_orders()`
* **Query Params:** `status` *(optional)*
* **Response Example:**

```json
{
  "success": true,
  "data": [
    {"id": 101, "customer": "Dept of Engr", "status": "In Production", "total_amount": 37500},
    {"id": 102, "customer": "Science Dept", "status": "Created", "total_amount": 24500}
  ]
}
```

---

#### **GET /api/orders/{order_id}**

* **Purpose:** Retrieve full order details (items, production, delivery, billing).
* **Service:** `order_service.get_order_details()`
* **Response Example:**

```json
{
  "success": true,
  "data": {
    "id": 101,
    "customer": "Dept of Engr",
    "items": [{"product": "Mapúa Hoodie", "quantity": 50}],
    "production": {"status": "Completed"},
    "delivery": {"status": "Pending"},
    "billing": null
  }
}
```

---

#### **POST /api/orders**

* **Purpose:** Create a new sales order with multiple items.
* **Service:** `order_service.create_order_with_items()`
* **Request Example:**

```json
{
  "customer_id": 1,
  "items": [
    {"product_id": 1, "quantity": 50},
    {"product_id": 2, "quantity": 20}
  ]
}
```

* **Response Example:**

```json
{
  "success": true,
  "data": {"id": 101, "total_amount": 37500, "status": "Created"}
}
```

---

#### **PATCH /api/orders/{order_id}/status**

* **Purpose:** Update order status (e.g., admin override or cancel).
* **Service:** `order_service.update_order_status()`
* **Request Example:**

```json
{"status": "Cancelled"}
```

---

#### **DELETE /api/orders/{order_id}**

* **Purpose:** Delete/cancel a sales order.
* **Service:** `order_service.delete_order()`

---

### ⚙️ **Production Orders API (`/api/production-orders`)**

#### **GET /api/production-orders?status=**

* **Purpose:** List all production orders (optionally filtered).
* **Service:** `production_service.list_production_orders()`
* **Response Example:**

```json
{
  "success": true,
  "data": [
    {"id": 3001, "sales_order_id": 101, "status": "Planned"},
    {"id": 3002, "sales_order_id": 102, "status": "In Progress"}
  ]
}
```

---

#### **POST /api/production-orders**

* **Purpose:** Start production for a given sales order.
* **Service:** `production_service.start_production_for_order()`
* **Request Example:**

```json
{"sales_order_id": 101}
```

---

#### **PATCH /api/production-orders/{id}/start**

* **Purpose:** Mark a production order as "In Progress".
* **Service:** `production_service.mark_production_in_progress()`

---

#### **PATCH /api/production-orders/{id}/complete**

* **Purpose:** Mark production complete, update related sales order.
* **Service:** `production_service.mark_production_complete()`

---

### 🚚 **Deliveries API (`/api/deliveries`)**

#### **GET /api/deliveries?status=**

* **Purpose:** List deliveries (optionally filtered).
* **Service:** `delivery_service.list_deliveries()`
* **Response Example:**

```json
{
  "success": true,
  "data": [
    {"id": 4001, "sales_order_id": 101, "status": "Pending"},
    {"id": 4002, "sales_order_id": 102, "status": "Delivered"}
  ]
}
```

---

#### **POST /api/deliveries**

* **Purpose:** Create delivery for completed production.
* **Service:** `delivery_service.create_delivery_for_order()`
* **Request Example:**

```json
{"sales_order_id": 101, "delivery_date": "2025-10-09"}
```

---

#### **PATCH /api/deliveries/{id}/complete**

* **Purpose:** Mark delivery as completed and update sales order.
* **Service:** `delivery_service.mark_delivery_done()`

---

### 💵 **Billing API (`/api/billings`)**

#### **GET /api/billings**

* **Purpose:** Retrieve all billing records.
* **Service:** `billing_service.list_billings()`
* **Response Example:**

```json
{
  "success": true,
  "data": [
    {"id": 5001, "sales_order_id": 101, "invoice_number": "INV-2025-001", "amount": 37500}
  ]
}
```

---

#### **POST /api/billings**

* **Purpose:** Generate a billing record after delivery.
* **Service:** `billing_service.generate_billing_for_order()`
* **Request Example:**

```json
{"sales_order_id": 101}
```

---

#### **GET /api/billings/{id}**

* **Purpose:** Retrieve specific billing record.
* **Service:** `billing_service.get_billing_for_order()`

---

### 🏷️ **Products API (`/api/products`)**

#### **GET /api/products?search=**

* **Purpose:** Retrieve full product catalog, optionally filter by keyword.
* **Service:** `product_service.get_product_catalog()`

---

#### **POST /api/products**

* **Purpose:** Add a new product.
* **Service:** `product_service.create_product_with_stock()`
* **Request Example:**

```json
{"name": "Mapúa Hoodie", "description": "Red cotton hoodie", "price": 750.00, "stock_qty": 100}
```

---

### 👤 **Customers API (`/api/customers`)**

#### **GET /api/customers?search=**

* **Purpose:** List all customers, with optional search.
* **Service:** `customer_service.list_customers()`
* **Response Example:**

```json
{
  "success": true,
  "data": [
    {"id": 1, "name": "Dept of Engineering", "role": "department"},
    {"id": 2, "name": "Juan Dela Cruz", "role": "student"}
  ]
}
```

---

### 📊 **Dashboard API (`/api/dashboard/summary`)**

#### **GET /api/dashboard/summary**

* **Purpose:** Aggregate KPIs for admin dashboard.
* **Service:** Aggregated counts via multiple repositories.
* **Response Example:**

```json
{
  "success": true,
  "data": {
    "total_orders": 120,
    "in_production": 15,
    "ready_for_delivery": 10,
    "billed": 90,
    "top_products": [{"name": "Mapúa Hoodie", "orders": 45}],
    "recent_orders": [{"id": 101, "customer": "Engr Dept", "status": "Billed"}]
  }
}
```

---

## 8. Implementation Plan

| Phase | Task                    | Description                              |
| ----- | ----------------------- | ---------------------------------------- |
| **1** | Router structure        | Create one router file per domain module |
| **2** | Define endpoints        | Match definitions in this PRD            |
| **3** | Integrate with services | Call service-layer functions only        |
| **4** | Add Pydantic schemas    | Define `Request` and `Response` models   |
| **5** | Register in main app    | Use `include_router()` in `app/main.py`  |
| **6** | Test                    | Verify via Swagger and Postman           |

---

## 9. Acceptance Criteria

| Criteria                        | Description                         |
| ------------------------------- | ----------------------------------- |
| ✅ All endpoints implemented     | Routes match frontend PRD           |
| ✅ Connected to service layer    | No direct ORM/repo usage in routers |
| ✅ Consistent responses          | `success`/`error` format everywhere |
| ✅ Error handling works          | 404/400/500 correctly mapped        |
| ✅ No pagination                 | Full lists returned                 |
| ✅ Swagger documentation visible | FastAPI auto-docs all routes        |

---

## 10. Future Enhancements

| Enhancement           | Description                                                     |
| --------------------- | --------------------------------------------------------------- |
| Authentication & RBAC | Add JWT auth for staff vs. customer access                      |
| Pagination            | Optional reintroduction for scaling beyond thousands of records |
| Real-time Updates     | Add WebSocket/SignalR for live order tracking                   |
| Async Implementation  | Convert routers and services to async for performance           |
| Versioning            | Introduce `/api/v2/` for future schema changes                  |

---

✅ **Summary**

This PRD defines the **API Endpoint Layer** for your MTO backend, completing the architecture stack.
It provides:

* Full CRUD + workflow coverage for all MTO modules
* Non-paginated, filterable list endpoints
* Clean separation of concerns (Router → Service → Repository)
* A structure ready for your Next.js frontends