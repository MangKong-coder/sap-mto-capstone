# PRD: Repository-Level CRUD Operations

## 1. Objective

Define repository-level CRUD operations for all entities in `models.py`. These will form the persistence layer, enabling the service layer to apply business logic on top (e.g., make-to-order flow, production tracking, deliveries, invoicing).

---

## 2. Entities and CRUD Requirements

### **Customer**

**Background:** Represents customers placing orders. Each customer can have multiple orders.
**CRUD Operations:**

* `create_customer(db, data)`
* `get_customer_by_id(db, customer_id)`
* `list_customers(db, skip=0, limit=10)`
* `update_customer(db, customer_id, data)`
* `delete_customer(db, customer_id)`

---

### **Product**

**Background:** Finished goods sold to customers. Linked to `OrderItem`.
**CRUD Operations:**

* `create_product(db, data)`
* `get_product_by_id(db, product_id)`
* `list_products(db, skip=0, limit=10)`
* `update_product(db, product_id, data)`
* `delete_product(db, product_id)`

---

### **Order**

**Background:** Sales orders placed by customers. Connected to order items, deliveries, invoices, and planned production.
**CRUD Operations:**

* `create_order(db, data)`
* `get_order_by_id(db, order_id)`
* `list_orders(db, skip=0, limit=10)`
* `update_order(db, order_id, data)`
* `delete_order(db, order_id)`

---

### **OrderItem**

**Background:** Line items of an order, referencing products and quantities. Foundation for planned/production orders.
**CRUD Operations:**

* `create_order_item(db, data)`
* `get_order_item_by_id(db, item_id)`
* `list_order_items(db, skip=0, limit=10)`
* `update_order_item(db, item_id, data)`
* `delete_order_item(db, item_id)`

---

### **PlannedOrder**

**Background:** Represents a planned production order before conversion into a work order. Tied to order items and sales orders.
**CRUD Operations:**

* `create_planned_order(db, data)`
* `get_planned_order_by_id(db, planned_id)`
* `list_planned_orders(db, skip=0, limit=10)`
* `update_planned_order(db, planned_id, data)`
* `delete_planned_order(db, planned_id)`

---

### **WorkOrder**

**Background:** Execution-level production orders derived from planned orders. Tracks progress, status, and component usage.
**CRUD Operations:**

* `create_work_order(db, data)`
* `get_work_order_by_id(db, work_id)`
* `list_work_orders(db, skip=0, limit=10)`
* `update_work_order(db, work_id, data)`
* `delete_work_order(db, work_id)`

---

### **Component**

**Background:** Raw materials/components used in work orders.
**CRUD Operations:**

* `create_component(db, data)`
* `get_component_by_id(db, component_id)`
* `list_components(db, skip=0, limit=10)`
* `update_component(db, component_id, data)`
* `delete_component(db, component_id)`

---

### **ComponentUsage**

**Background:** Tracks how many components are consumed by each work order.
**CRUD Operations:**

* `create_component_usage(db, data)`
* `get_component_usage_by_id(db, usage_id)`
* `list_component_usages(db, skip=0, limit=10)`
* `update_component_usage(db, usage_id, data)`
* `delete_component_usage(db, usage_id)`

---

### **Delivery**

**Background:** Represents shipment of goods to customers, linked to orders. Tracks delivery status and quantities.
**CRUD Operations:**

* `create_delivery(db, data)`
* `get_delivery_by_id(db, delivery_id)`
* `list_deliveries(db, skip=0, limit=10)`
* `update_delivery(db, delivery_id, data)`
* `delete_delivery(db, delivery_id)`

---

### **Invoice**

**Background:** Billing records tied to orders. Tracks invoice date, amount, and payment status.
**CRUD Operations:**

* `create_invoice(db, data)`
* `get_invoice_by_id(db, invoice_id)`
* `list_invoices(db, skip=0, limit=10)`
* `update_invoice(db, invoice_id, data)`
* `delete_invoice(db, invoice_id)`

---

### **OrderComponentUsage (View)**

**Background:** A read-only aggregated view showing total component usage per order.
**CRUD Operations:**

* `list_order_component_usage(db, order_id=None)` (read-only)

---

## 3. Error Handling

* Return `None` if record not found.
* Integrity errors (e.g., foreign key or unique violations) surfaced for service layer handling.

---

## 4. Deliverables

* Repository files under `app/repositories/`.
* CRUD functions implemented per entity.
* Read-only accessor for the aggregated component usage view.
