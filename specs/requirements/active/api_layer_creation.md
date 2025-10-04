# 📑 Product Requirements Document (PRD)

**Feature:** API Layer for MTO (Make-to-Order) Capstone Backend
**Owner:** Backend Team
**Status:** Draft

---

## 1. Background & Context

The capstone system models a **Make-to-Order manufacturing flow** inspired by SAP modules (PP, SD, MM).
We already have:

* **Repository Layer:** CRUD access to database.
* **Service Layer:** Business logic (validations, flow orchestration).

The next step is to build an **API Layer** that exposes the system functionality for the frontend (Fiori-like dashboard). The API must be RESTful, modular, and align with immutability principles (no hard deletes).

---

## 2. Goals & Objectives

* Provide a **RESTful API** that exposes all business logic from the service layer.
* Ensure the endpoints are **consistent, predictable, and secure-ready**.
* Enable the frontend to:

  * Create and manage orders, products, customers.
  * Track planned orders, work orders, deliveries, invoices.
  * View reporting summaries across the MTO flow.
* Maintain **immutability**: entities are never deleted, only updated/canceled/closed.

---

## 3. Scope

### In-Scope

* Implementation of all API endpoints (see Section 5).
* Use of FastAPI routers grouped by domain (`orders`, `customers`, `products`, etc.).
* Pagination on all list endpoints.
* Error handling aligned with service-layer exceptions.

### Out-of-Scope

* Authentication/authorization (to be stubbed if needed).
* Advanced filtering/search (beyond pagination).
* UI/dashboard integration (handled by frontend team).

---

## 4. Success Metrics

* **Functional completeness:** All service functions are accessible via API.
* **Consistency:** All endpoints follow RESTful conventions (`GET`, `POST`, `PUT`).
* **Reliability:** Proper error codes returned (`404` for not found, `400` for validation, etc.).
* **Usability:** Frontend can perform end-to-end MTO flow (order → production → delivery → invoice).

---

## 5. API Endpoints Specification

### Components

* `POST /components` → Add new component
* `PUT /components/{component_id}` → Update details
* `GET /components/{component_id}` → Get by ID
* `GET /components/code/{part_code}` → Get by part code
* `GET /components/{component_id}/availability` → Check availability
* `GET /components` → List components (pagination)

---

### Component Usage

* `POST /component-usage` → Record usage against work order
* `GET /component-usage/{usage_id}` → Get by ID
* `GET /component-usage/work-order/{work_order_id}` → List by work order
* `GET /component-usage/component/{component_id}` → List by component
* `GET /component-usage/order/{order_id}/summary` → Summarize usage for an order
* `GET /component-usage` → List all usages (pagination)

---

### Customers

* `POST /customers` → Register customer
* `PUT /customers/{customer_id}` → Update profile
* `GET /customers/{customer_id}` → Get by ID
* `GET /customers/{customer_id}/orders` → Get orders
* `GET /customers` → List customers (pagination)

---

### Orders

* `POST /orders` → Place new order
* `PUT /orders/{order_id}/cancel` → Cancel order
* `GET /orders/{order_id}` → Get order by ID
* `GET /orders/{order_id}/status` → Get order status
* `GET /orders/{order_id}/planned-orders` → List planned orders
* `GET /orders/{order_id}/deliveries` → List deliveries
* `GET /orders/{order_id}/invoices` → List invoices
* `GET /orders/customer/{customer_id}` → List by customer
* `GET /orders` → List orders (pagination)

---

### Planned Orders

* `POST /planned-orders` → Generate from order item
* `PUT /planned-orders/{planned_order_id}` → Update status/details
* `PUT /planned-orders/{planned_order_id}/convert` → Convert → work order
* `GET /planned-orders/{planned_order_id}` → Get by ID
* `GET /planned-orders` → List all planned orders

---

### Work Orders

* `PUT /work-orders/{work_order_id}/start` → Start work order
* `PUT /work-orders/{work_order_id}/confirm` → Confirm completion
* `PUT /work-orders/{work_order_id}/consume` → Record component consumption
* `PUT /work-orders/{work_order_id}/close` → Close work order
* `GET /work-orders/{work_order_id}` → Get work order by ID
* `GET /work-orders/{work_order_id}/usage` → Get component usage for work order
* `GET /work-orders` → List work orders (pagination)

---

### Deliveries

* `POST /deliveries` → Schedule delivery
* `PUT /deliveries/{delivery_id}/status` → Update status
* `GET /deliveries/{delivery_id}` → Get by ID
* `GET /deliveries/customer/{customer_id}` → List deliveries for customer
* `GET /deliveries/order/{order_id}` → List deliveries for order
* `GET /deliveries` → List deliveries (pagination)

---

### Invoices

* `POST /invoices` → Generate invoice
* `PUT /invoices/{invoice_id}/pay` → Mark as paid
* `PUT /invoices/{invoice_id}/post` → Post (DRAFT → POSTED)
* `PUT /invoices/{invoice_id}/cancel` → Cancel invoice
* `GET /invoices/{invoice_id}` → Get by ID
* `GET /invoices/customer/{customer_id}/outstanding` → Get unpaid invoices
* `GET /invoices/order/{order_id}` → List invoices for order
* `GET /invoices` → List invoices (pagination)

---

### Products

* `POST /products` → Add new product
* `PUT /products/{product_id}` → Update details
* `GET /products/{product_id}` → Get by ID
* `GET /products/sku/{sku}` → Get by SKU
* `GET /products/{product_id}/availability` → Check availability
* `GET /products` → List products (pagination)

---

### Reporting

* `GET /reporting/orders/{order_id}/flow` → Trace order through full MTO flow
* `GET /reporting/production-status` → Summarize work order statuses
* `GET /reporting/component-consumption` → Aggregate component usage
* `GET /reporting/orders/{order_id}/component-usage` → Get order component usage summary
* `GET /reporting/customers/{customer_id}/summary` → Customer order summary
* `GET /reporting/orders/summary` → Legacy order summary

---

### MTO Flow Automation

* `POST /mto/auto-production-order` → Auto-create production order from sales order

---

## 6. Acceptance Criteria

* [ ] All endpoints implemented and routed through FastAPI.
* [ ] Each router grouped by domain (`/orders`, `/products`, etc.).
* [ ] JSON request/response schemas defined using Pydantic.
* [ ] Validation errors return `400 Bad Request`.
* [ ] Missing entities return `404 Not Found`.
* [ ] Business logic violations (e.g., canceling a closed order) return `409 Conflict`.
* [ ] Pagination query params standardized (`?page=1&size=20`).
* [ ] End-to-end test: place order → planned order → work order → delivery → invoice → reporting.

---

## 7. Risks & Mitigations

* **Risk:** Too many endpoints may overwhelm frontend.

  * *Mitigation:* Provide reporting APIs to reduce frontend aggregation.
* **Risk:** Without auth, APIs are open.

  * *Mitigation:* Add stubbed middleware for later RBAC if required.
* **Risk:** Time constraints may prevent bonus features (BOM, routing).

  * *Mitigation:* Keep scope to MTO core flow.
