# PRD: Service Layer Functions

## 1. Objective

To implement the **service layer** on top of the repository CRUD operations. This layer enforces **business rules** and coordinates between multiple repositories to execute the **Make-to-Order (MTO) manufacturing flow**.

The service layer ensures that system processes follow the intended logic:

* Sales orders trigger planned orders.
* Planned orders convert to work orders.
* Work orders consume components and produce finished goods.
* Deliveries and invoices are generated at the right stage.

---

## 2. Scope

* **In-Scope**

  * Define and implement service functions for all entities in `models.py`.
  * Handle business workflows like order placement, production confirmation, and delivery.
  * Provide read-only aggregation/reporting functions to track system status.

* **Out-of-Scope**

  * Low-level database operations (handled by repositories).
  * API endpoints (controller layer).
  * Authentication, authorization, or user session management.

---

## 3. Service Functions by Entity

### **Customer Service**

Manages customer lifecycle.

* `register_customer(data)` – create new customer with validation.
* `update_customer_profile(customer_id, data)` – enforce uniqueness, prevent invalid changes.
* `get_customer_orders(customer_id)` – retrieve all orders linked to a customer.

---

### **Product Service**

Manages product catalog and stock.

* `add_new_product(data)` – enforce SKU uniqueness.
* `update_product_stock(product_id, qty)` – adjust stock after production/delivery.
* `get_product_availability(product_id)` – check if stock is available.

---

### **Order Service**

Handles sales order lifecycle.

* `place_order(customer_id, items)` – validate products + stock, create order and items.
* `cancel_order(order_id)` – only if not yet delivered or in production.
* `get_order_status(order_id)` – consolidated status across production/delivery/invoice.
* `list_orders_by_customer(customer_id)` – fetch all orders for a given customer.

---

### **Planned Order Service**

Coordinates planning from sales to production.

* `generate_planned_order(order_item_id)` – auto-generate planned order.
* `update_planned_order(planned_id, status)` – modify status/details.
* `convert_to_work_order(planned_id)` – create work order from planned order.

---

### **Work Order Service**

Manages production execution.

* `start_work_order(work_id)` – set to “In Progress”.
* `confirm_work_order(work_id, produced_qty)` – complete work, update inventory.
* `consume_components(work_id, components)` – deduct raw material usage.
* `close_work_order(work_id)` – finalize after confirmation.

---

### **Component Service**

Tracks raw material availability.

* `add_component(data)` – register raw material.
* `update_component_stock(component_id, qty)` – adjust inventory.
* `get_component_availability(component_id)` – check stock levels.

---

### **Component Usage Service**

Logs material consumption in production.

* `record_component_usage(work_id, component_id, qty_used)` – log usage against work order.
* `get_usage_by_work_order(work_id)` – fetch all component usage for a work order.
* `summarize_component_usage(order_id)` – aggregate usage per order (using view).

---

### **Delivery Service**

Manages customer deliveries.

* `schedule_delivery(order_id, details)` – create delivery once goods are produced.
* `update_delivery_status(delivery_id, status)` – track logistics.
* `get_customer_deliveries(customer_id)` – fetch delivery history.

---

### **Invoice Service**

Handles billing.

* `generate_invoice(order_id)` – generate invoice after delivery.
* `mark_invoice_paid(invoice_id)` – confirm payment.
* `get_outstanding_invoices(customer_id)` – track unpaid invoices.

---

### **Reporting / Aggregation Services**

Provides cross-entity insights.

* `get_order_full_flow(order_id)` – trace order through production → delivery → invoice.
* `get_production_status_summary()` – summarize work order statuses.
* `get_component_consumption_summary()` – aggregate raw material usage.

---

## 4. Error Handling

* Validation errors raised at service level (e.g., insufficient stock, invalid cancellation).
* Repository errors (e.g., integrity issues) surfaced as domain-level exceptions.
* Services return either data objects or meaningful error responses for the API layer.

---

## 5. Deliverables

* Service modules in `app/services/` directory.
* One service file per entity (`customer_service.py`, `order_service.py`, etc.).
* Reporting functions under `reporting_service.py`.
* Unit-testable service functions independent of the API.

---

## 6. Next Steps

* Implement service functions based on repository layer.
* Build API endpoints that consume these services.
* Integrate workflows (MTO flow, production tracking, billing cycle) into end-to-end processes.