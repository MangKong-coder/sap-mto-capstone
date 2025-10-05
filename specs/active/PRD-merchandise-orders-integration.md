# PRD: Merchandise Orders Page ↔ Backend Integration

## Objective
- **Goal**: Connect the frontend Merchandise Orders experience to the backend orders domain to support listing, creating, inspecting, and managing merchandise (sales) orders.
- **Outcomes**:
  - Users can view a paginated list of merchandise orders with enriched customer/product info.
  - Users can create a merchandise order using real customers/products and see it appear in the list.
  - Users can view real order details and document flow (planned orders, production, delivery, billing) from backend data.
  - Users can cancel an order when allowed, with clear error feedback when not allowed.

## Scope
- **In-scope (MVP)**
  - Wire `Merchandise Orders` page to backend using existing DAL and endpoints.
  - Implement pagination, filtering on client side.
  - Implement order creation via backend (`POST /orders`).
  - Implement details modal showing real details plus document flow using backend (`GET /orders/{id}/status`).
  - Error handling and UX feedback (loading, empty, error, toasts).
- **Out-of-scope (MVP)**
  - Editing orders beyond cancellation.
  - Bulk actions.
  - Server-side filtering/sorting.
  - Real-time updates via websockets.

## Background and Current State
- **Frontend files**
  - `mto-frontend/app/sales-orders/page.tsx`: The Merchandise Orders page shell with search and a "Create Merchandise Order" dialog.
  - `mto-frontend/components/sales-order-table.tsx`: Loads orders via `getOrders(page, size)` from `@/lib/dal` and renders a table. Supports client-side filtering.
  - `mto-frontend/components/create-sales-order-dialog.tsx`: Loads customers/products and calls `createOrder()` with mapped payload.
  - `mto-frontend/components/sales-order-details-dialog.tsx`: Displays order info and a mocked document flow derived from `orderNumber`.
  - `mto-frontend/lib/dal/orders.ts`: Implements API calls to: `GET /orders/enriched`, `GET /orders/{id}/enriched`, `POST /orders`, `PUT /orders/{id}/cancel`, `GET /orders/customer/{id}`. Includes `transformBackendOrder()` mapping to `SalesOrder` type defined in `mto-frontend/lib/types.ts`.
- **Backend files**
  - `mto-backend/app/api/routes/orders.py`: Full orders API surface including enriched list/detail, status, cancel, by-customer.
  - `mto-backend/app/services/order_service.py`: Business logic; provides enriched responses and consolidated status.
  - `mto-backend/app/crud/repositories/orders.py`: Optimized eager-loading queries for enriched payloads.
  - Schemas: `mto-backend/app/schemas/order.py` (`OrderCreate`, `OrderResponse`, `OrderEnrichedResponse`, `OrderStatusResponse`) and related.

## Target UX Flows
- **List Orders**
  - On page load, fetch paginated enriched orders. Show loading, then table or empty state/error.
  - Client-side search filters by order number, customer, or material.
  - Pagination controls allow moving through pages.
- **Create Order**
  - Dialog loads customers/products. User selects customer type, customer, product, quantity, delivery date, priority, and plant.
  - Submit creates order; on success: toast, dialog closes, table refreshes.
  - Handle validation errors (400) with actionable feedback.
- **Order Details and Document Flow**
  - Clicking "View" opens details modal.
  - On open, fetch consolidated status via `GET /orders/{id}/status`.
  - Display work orders, deliveries, invoices if present with IDs/statuses and dates.
- **Cancel Order (optional in MVP UI)**
  - If exposed, calling cancel shows success or reason why cancel is blocked (409), eg work orders in progress or deliveries exist.

## API Contracts (Backend)
Base path: `${NEXT_PUBLIC_API_URL || http://localhost:8000}/api/v1`

- **List Enriched Orders**
  - Endpoint: `GET /orders/enriched?page={page}&size={size}`
  - Response: `List[Dict]` matching `OrderEnrichedResponse`, with keys:
    - `id`, `customer_id`, `customer_name`, `customer_type`, `status`, `order_date`, `delivery_date`, `priority`, `work_center_id`, `work_center_name`, `items` (list of `{id, product_id, product_sku, product_name, quantity, unit_price}`), `total_quantity`, `net_value`, `created_at`, `updated_at`.
- **Get Single Enriched Order**
  - Endpoint: `GET /orders/{order_id}/enriched`
  - 404 if not found.
- **Get Consolidated Order Status (Document Flow)**
  - Endpoint: `GET /orders/{order_id}/status`
  - Response `OrderStatusResponse` includes: `order_id`, `status`, `order_date`, `delivery_date`, `customer_id`, `items_count`, `work_orders` (`[{id,status,quantity,start_date,end_date}]`), `deliveries` (`[{id,status,quantity,delivered_at}]`), `invoices` (`[{id,status,total_amount,invoice_date}]`).
- **Create Order**
  - Endpoint: `POST /orders`
  - Body `OrderCreate`: `{ customer_id: int, delivery_date?: datetime, priority?: "STANDARD"|"URGENT"|"RUSH", work_center_id: int, items: [{ product_id: int, quantity: number, unit_price?: number }] }`
  - Responses: `201 OrderResponse` on success. `400` on validation error.
- **Cancel Order**
  - Endpoint: `PUT /orders/{order_id}/cancel`
  - Responses: `200 OrderResponse` on success; `404` if not found; `409` if cannot cancel (in progress/completed/delivered).
- **List Orders by Customer**
  - Endpoint: `GET /orders/customer/{customer_id}`

Related (for future UI growth): `planned-orders` endpoints including `PUT /planned-orders/{id}/convert` (returns `WorkOrderResponse`).

## Frontend Data Mapping
- **Type**: `mto-frontend/lib/types.ts` `SalesOrder`
  - `{ id: string, orderNumber: string, customer: string, customerType: "Department"|"Campus", material: string, quantity: number, deliveryDate: string, status: "Open"|"In Planning"|"In Production"|"Delivered"|"Billed", createdDate: string, netValue: number, plant: string, priority: "Standard"|"Urgent"|"Rush" }`
- **Mapping (`transformBackendOrder()` in `lib/dal/orders.ts`)**
  - `id` → `backendOrder.id.toString()`.
  - `orderNumber` → stringified `id`.
  - `customer` → `customer_name`.
  - `customerType` → `'Department'` if `customer_type==='DEPARTMENT'` else `'Campus'`.
  - `material` → first `items[].product_name` else `"Multiple Items"`.
  - `quantity` → `total_quantity`.
  - `deliveryDate` → `delivery_date` (fallback to now if missing).
  - `status` → mapped from backend `OrderStatus` using `mapBackendStatus()`.
  - `createdDate` → `created_at`.
  - `netValue` → `net_value`.
  - `plant` → `work_center_name`.
  - `priority` → mapped from backend enum using `mapBackendPriority()`.

## Required Frontend Work
- **[DAL] Add status retrieval**
  - Add `getOrderStatus(orderId: string)` calling `GET /orders/{id}/status`.
  - Define a minimal TypeScript type for the response to render the document flow.
- **[Details Modal] Use real document flow**
  - In `components/sales-order-details-dialog.tsx`, on open, fetch `getOrderStatus(order.id)` and render real `work_orders`, `deliveries`, `invoices` instead of mocked `PO-/PRO-/DL-/INV-` placeholders.
  - Show loading indicator inside the dialog while fetching; handle error gracefully with a small inline notice.
- **[Table] Pagination controls**
  - `components/sales-order-table.tsx` already tracks `currentPage`. Add UI controls (Prev/Next, page size if needed).
  - Pass `currentPage` to `getOrders(page, size)` (already done) and refresh on page change.
- **[Create Dialog] Validation and mapping**
  - Ensure `priority` is uppercased before submit (already done).
  - Ensure `work_center_id` mapping is correct; expose a stable mapping source (later improvement: fetch work centers instead of hardcoding).
  - On success, invoke parent `onOrderCreated()` to refresh table (already implemented).
- **[Cancel Action] (Optional)**
  - If exposing cancel: add a cancel menu action per row calling `cancelOrder(order.id)` and surface `404/409` messages.

## Non-Functional Requirements
- **Performance**: Use enriched list endpoints that eager-load relationships to avoid N+1. Page size default 20; do not request more than 100 per backend constraint.
- **Resilience**: All network calls display loading and error states (`sales-order-table.tsx` has base patterns to follow).
- **Config**: Base URL configured via `NEXT_PUBLIC_API_URL` in env; default `http://localhost:8000/api/v1`.
- **Consistency**: Match existing status/priority mappings in `lib/dal/orders.ts`.
- **Accessibility**: Dialogs and buttons use accessible labels; maintain keyboard navigation.

## Detailed Implementation Plan
- **1) DAL** (`mto-frontend/lib/dal/orders.ts`)
  - Add:
    - `export async function getOrderStatus(orderId: string): Promise<{ order_id: number; status: string; work_orders: any[]; deliveries: any[]; invoices: any[]; order_date?: string; delivery_date?: string; items_count: number; }>`.
- **2) Details Dialog** (`components/sales-order-details-dialog.tsx`)
  - Add local state: `{ loading, error, statusData }`.
  - `useEffect` on `open && order?.id` → call `getOrderStatus(order.id)`, set state.
  - Render document flow from `statusData` lists; display IDs and statuses with dates.
- **3) Table Pagination** (`components/sales-order-table.tsx`)
  - Add simple pagination controls below table.
  - Disable Prev on page 1; disable Next when `filteredOrders.length < pageSize`.
- **4) Create Dialog** (`components/create-sales-order-dialog.tsx`)
  - Keep current mapping; validate `quantity` > 0, `plant` required, `customerType` gating of customers.
  - Consider lifting hardcoded plant map to a constant near top.
- **5) Optional: Cancel Action** (`components/sales-order-table.tsx`)
  - Row action → call `cancelOrder()`; refresh table on success; display error message on 409.

## Acceptance Criteria
- **List**
  - Displays first page of orders from `GET /orders/enriched` with all columns populated per mapping.
  - Pagination controls navigate pages and trigger new fetch.
  - Search filters results by order number, customer, and material client-side.
- **Create**
  - Submitting valid data calls `POST /orders` and success toast appears; dialog closes; table refreshes and newly created order can be found.
  - Invalid submissions show backend error messages (e.g., product/customer not found).
- **Details**
  - Opening details calls `GET /orders/{id}/status`; shows real work orders, deliveries, and invoices if present; shows empty-state when none.
  - Loading and error states are visible and non-blocking.
- **Cancel (if enabled)**
  - Cancel succeeds for eligible orders; shows toast and updates status.
  - Ineligible cancelations show specific reason (409) from backend.

## Test Plan
- **Unit (frontend)**
  - DAL unit tests for `getOrderStatus()` mapping and error handling.
  - Component tests for `sales-order-table` (pagination/search) and `sales-order-details-dialog` (loading/error/render of status data).
- **Integration (manual and/or e2e)**
  - Seed environment; verify list population and pagination.
  - Create order through dialog; confirm appears on list and details render correctly.
  - Attempt cancel on different statuses to exercise `404/409` paths.
- **Backend**
  - Verify `orders.py` endpoints return expected schemas (`OrderEnrichedResponse`, `OrderStatusResponse`).

## Risks & Mitigations
- **Hardcoded work center mapping**: Might misalign with actual DB IDs. Mitigate by introducing `GET /work-centers` and a selector (future scope).
- **Date/time handling**: Ensure timezone consistency; display using locale formatting (already implemented in components).
- **Large datasets**: Keep page size reasonable; enable server-side filtering in future.

## Rollout
- Feature flags: Not required.
- Deployment: Frontend + backend can ship independently; ensure `NEXT_PUBLIC_API_URL` is configured in environments.
- Monitoring: Console errors and API response codes during manual UAT.

## Open Questions
- Should we expose cancel in the table UI now, or defer?
- Do we need server-side filtering/sorting soon for large datasets?
- Should the details modal show nested item-level production/delivery breakdowns?
