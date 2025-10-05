# Backend Overview

## Technology Stack
- **FastAPI** – Backend framework for building APIs.
- **PostgreSQL** – Relational database for storing and managing project data.
- **SQLAlchemy/SQLModel** – ORM for defining models and interacting with the database.
- **Pydantic** – Data validation and serialization.

## Responsibilities of the Backend
The backend acts as the **engine of the MTO system**, managing data, business logic, and process flow. Its main roles include:

1. **Database Management**
   - Defines entities like `SalesOrder`, `PlannedOrder`, `ProductionOrder`, `Delivery`, and `Billing`.
   - Ensures data consistency using foreign keys and status enums.
   - Provides audit fields (`created_at`, `updated_at`) for all major tables.

2. **Business Logic**
   - Handles order progression from Sales → Planned → Production → Delivery → Billing.
   - Updates statuses (e.g., `PENDING`, `IN_PROGRESS`, `COMPLETED`).
   - Validates relationships (e.g., production orders must be tied to a sales order).

3. **API Functionality**
   - **Sales Orders**: CRUD endpoints with pagination.
   - **Planned Orders**: Auto-generated from sales orders.
   - **Production Orders**: Conversion, tracking, and status updates.
   - **Deliveries**: Linking production completion to shipment.
   - **Billing**: Generating billing records after delivery.
   - **Reports/Views**: Exposing aggregated data like production progress.

4. **Security and Roles (Optional)**
   - Basic authentication and role-based access (e.g., Admin, Planner, Sales).
   - Ensures only authorized users can perform certain actions.

## Example Flow
1. A user creates a **Sales Order**.
2. The backend auto-generates a **Planned Order**.
3. The planner converts it into a **Production Order**.
4. The production team updates progress until it’s **Completed**.
5. The backend creates a **Delivery record**.
6. A **Billing record** is issued and linked to the sales order.

## Why This Matters
The backend provides the **core functionality** of the system. It ensures that all transactions are connected, statuses are updated properly, and data flows smoothly from customer order to final billing.
