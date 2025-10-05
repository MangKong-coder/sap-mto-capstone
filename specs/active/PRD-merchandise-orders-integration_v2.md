# PRD v2: Merchandise Orders ↔ Backend Integration

Version: 2.0
Owner: Engineering
Status: Draft

## 1) Summary
- Connect the `Merchandise Orders` experience to backend Orders so users can list, create, inspect, and (optionally) cancel orders using real data.
- Replace mocked document flow with live consolidated status from backend.

## 2) Goals
- **List** paginated orders with enriched customer/product/work center fields.
- **Create** orders via dialog and refresh the list on success.
- **Inspect** an order’s document flow (planned orders, work orders, deliveries, invoices) from backend status.
- **Cancel** orders when allowed (optional UI in MVP).

## 3) Non-Goals
- Editing orders beyond cancel.
- Bulk actions.
- Server-side search/sort (client-side only for now).
- Realtime updates.

## 4) Stakeholders
- Frontend: `mto-frontend` (Next.js app)
- Backend: `mto-backend` (FastAPI services)

## 5) Current State (as of repo scan)
- Page shell: `mto-frontend/app/sales-orders/page.tsx`
- List UI: `mto-frontend/components/sales-order-table.tsx` uses `getOrders(page, size)` and client search.
- Create UI: `mto-frontend/components/create-sales-order-dialog.tsx` calls `createOrder()`; fetches customers/products.
- Details UI: `mto-frontend/components/sales-order-details-dialog.tsx` shows mocked document flow.
- DAL: `mto-frontend/lib/dal/orders.ts` implements:
  - `getOrders`, `getOrderById`, `createOrder`, `cancelOrder`, `getOrdersByCustomer`.
  - Maps backend enriched order → `SalesOrder` (`mto-frontend/lib/types.ts`).
- Backend Orders API (`mto-backend/app/api/routes/orders.py`):
  - `GET /orders/enriched?page&size` (list)
  - `GET /orders/{id}/enriched` (detail)
  - `GET /orders/{id}/status` (consolidated status)
  - `POST /orders` (create)
  - `PUT /orders/{id}/cancel` (cancel)
  - `GET /orders/customer/{customer_id}` (by customer)
- Enriched shaping and status: `app/services/order_service.py` with eager loading from `app/crud/repositories/orders.py`.

## 6) User Flows
- **List**: On load, fetch page 1 (size 20). Show loading, error, empty. Client search filters by order number, customer, material. Pagination navigates pages.
- **Create**: Open dialog → select type/customer/product/qty/date/priority/plant → submit → success toast → dialog closes → list refreshes.
- **Details**: Click View → open modal → fetch `GET /orders/{id}/status` → render work orders, deliveries, invoices with IDs/status/dates → loading/error inside dialog.
- **Cancel (optional)**: Row action → call `PUT /orders/{id}/cancel` → handle 200/404/409; refresh and toast.

## 7) API Contracts (Backend)
Base: `${NEXT_PUBLIC_API_URL || http://localhost:8000}/api/v1`

- List Enriched Orders: `GET /orders/enriched?page={1..}&size={1..100}`
  - Returns `List` of objects (see enriched shape below).
- Get Enriched Order: `GET /orders/{order_id}/enriched`
  - 404 if not found.
- Get Consolidated Status: `GET /orders/{order_id}/status`
  - Returns `{ order_id, status, order_date?, delivery_date?, customer_id, items_count, work_orders[], deliveries[], invoices[] }`.
- Create Order: `POST /orders`
  - Body (Pydantic `OrderCreate`): `{ customer_id:number, delivery_date?:datetime, priority?:"STANDARD"|"URGENT"|"RUSH", work_center_id:number, items:[{ product_id:number, quantity:number, unit_price?:number }] }`.
  - 201 on success; 400 on validation errors.
- Cancel Order: `PUT /orders/{order_id}/cancel`
  - 200 success; 404 not found; 409 blocked (e.g., in progress or delivered).

### 7.1 Sample Payloads
- Enriched order (list item):
```json
{
  "id": 12,
  "customer_id": 3,
  "customer_name": "Intramuros Campus",
  "customer_type": "CAMPUS",
  "status": "NEW",
  "order_date": "2025-10-05T10:30:00Z",
  "delivery_date": "2025-10-20T00:00:00Z",
  "priority": "STANDARD",
  "work_center_id": 1,
  "work_center_name": "Intramuros Bookstore",
  "items": [
    {"id": 101, "product_id": 55, "product_sku": "SHIRT-001", "product_name": "UST Shirt", "quantity": 50, "unit_price": 350}
  ],
  "total_quantity": 50,
  "net_value": 17500,
  "created_at": "2025-10-05T10:30:10Z",
  "updated_at": "2025-10-05T10:30:10Z"
}
```
- Status response:
```json
{
  "order_id": 12,
  "status": "IN_PROGRESS",
  "order_date": "2025-10-05T10:30:00Z",
  "delivery_date": "2025-10-20T00:00:00Z",
  "customer_id": 3,
  "items_count": 1,
  "work_orders": [{"id": 9001, "status": "IN_PROGRESS", "quantity": 50, "start_date": "2025-10-07T02:00:00Z", "end_date": null}],
  "deliveries": [],
  "invoices": []
}
```
- Create order request:
```json
{
  "customer_id": 3,
  "delivery_date": "2025-10-20",
  "priority": "STANDARD",
  "work_center_id": 1,
  "items": [{"product_id": 55, "quantity": 50, "unit_price": 350}]
}
```

## 8) Frontend Data Mapping
- Type: `SalesOrder` in `mto-frontend/lib/types.ts`.
- Mapping in `mto-frontend/lib/dal/orders.ts` `transformBackendOrder()`:
  - `id` → `String(id)`
  - `orderNumber` → `String(id)`
  - `customer` → `customer_name`
  - `customerType` → `'Department'` if `DEPARTMENT` else `'Campus'`
  - `material` → first `items[].product_name` or `"Multiple Items"`
  - `quantity` → `total_quantity`
  - `deliveryDate` → `delivery_date || new Date().toISOString()`
  - `status` → via `mapBackendStatus()` (`NEW→Open`, `CONFIRMED→In Planning`, `IN_PROGRESS→In Production`, `COMPLETED→Delivered`, `BILLED→Billed`)
  - `createdDate` → `created_at`
  - `netValue` → `net_value`
  - `plant` → `work_center_name`
  - `priority` → via `mapBackendPriority()` (`STANDARD|URGENT|RUSH` → `Standard|Urgent|Rush`)

## 9) Detailed Implementation Plan

### 9.1 DAL (`mto-frontend/lib/dal/orders.ts`)
- Add `getOrderStatus(orderId: string)`:
```ts
export async function getOrderStatus(orderId: string): Promise<{
  order_id: number; status: string; order_date?: string; delivery_date?: string;
  customer_id: number; items_count: number;
  work_orders: { id:number; status:string; quantity:number; start_date?:string; end_date?:string }[];
  deliveries: { id:number; status:string; quantity:number; delivered_at?:string }[];
  invoices: { id:number; status:string; total_amount:number; invoice_date?:string }[];
}> {
  const res = await fetch(`${API_BASE}/orders/${orderId}/status`)
  if (!res.ok) throw new Error(`Failed to fetch status: ${res.status}`)
  return res.json()
}
```

### 9.2 Details Dialog (`mto-frontend/components/sales-order-details-dialog.tsx`)
- On open, fetch status and render real document flow.
- State: `{ loading, error, statusData }`.
- Pseudocode:
```tsx
useEffect(() => {
  if (!open) return
  let mounted = true
  setLoading(true); setError(null)
  getOrderStatus(order.id)
    .then((data) => { if (mounted) setStatusData(data) })
    .catch((e) => { if (mounted) setError(e.message) })
    .finally(() => mounted && setLoading(false))
  return () => { mounted = false }
}, [open, order?.id])
```
- Render lists for `work_orders`, `deliveries`, `invoices` with IDs, statuses, and dates; show loading/error inline.

### 9.3 Table Pagination (`mto-frontend/components/sales-order-table.tsx`)
- Add controls under table: Prev/Next.
- Disable Prev on page 1; Next when returned list length < pageSize.
- Keep client search (filter over fetched page).

### 9.4 Create Dialog (`mto-frontend/components/create-sales-order-dialog.tsx`)
- Keep existing mapping; ensure:
  - `priority` uppercased before submit (already handled).
  - `work_center_id` chosen via mapping constant (future: fetch work centers API).
  - `quantity > 0`, all required fields present.
- On success: toast, close, call `onOrderCreated()`.

### 9.5 Optional Cancel Action (table row)
- Row action → `cancelOrder(order.id)`; handle 200/404/409 with toast; refresh on success.

## 10) Errors & Edge Cases
- Network failures → show inline error messages and retry affordances.
- 400 on create → surface `detail` from backend (validation issues like missing product/customer).
- 404/409 on cancel → show specific reason text.
- Timezones → backend returns ISO; format with `toLocaleDateString()` in UI.
- Items missing product_name (unlikely) → fallback label `Multiple Items` (already handled).

## 11) Performance
- Use backend enriched endpoints with eager loading to avoid N+1.
- Default page size 20; cap at 100.
- Avoid fetching status until details dialog is opened.

## 12) Security
- Base URL via `NEXT_PUBLIC_API_URL` only; no secrets in client bundles.
- No PII beyond customer names; follow existing auth posture (if any) outside scope.

## 13) Telemetry (Optional)
- Log to console in dev for request/response failures.
- Future: hook to analytics for create and cancel actions.

## 14) Rollout
- No feature flag required.
- Validate in dev; ensure `.env` has `NEXT_PUBLIC_API_URL` matching backend.
- Ship frontend/backends independently; endpoint contracts are stable.

## 15) Acceptance Criteria
- List shows real data from `GET /orders/enriched` with correct mapping for columns.
- Pagination controls navigate and refetch.
- Create dialog successfully posts; new order visible after refresh.
- Details dialog fetches `GET /orders/{id}/status` on open and renders non-mocked flow.
- Optional cancel (if enabled) works and handles 404/409 with clear messages.

## 16) Test Plan
- Unit (frontend):
  - DAL: `getOrderStatus()` happy/404/error.
  - Components: table pagination logic; details dialog loading/error/render states.
- Manual/e2e:
  - Seed DB; verify listing/pagination.
  - Create order; verify appears with mapped fields.
  - Open details; verify work orders/deliveries/invoices render when present.
  - Try cancel various states to see 200/404/409 handling.

## 17) Risks & Mitigations
- Hardcoded `work_center_id` mapping may drift → add `GET /work-centers` later and drive from API.
- Large datasets → add server-side filters/sort in a follow-up.
- Schema drift → rely on backend `OrderEnrichedResponse`/`OrderStatusResponse` tests and contract review.
