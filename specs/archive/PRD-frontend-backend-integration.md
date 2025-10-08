# RFC / PRD: Frontend ↔ Backend Integration and Mock Removal (MTO Merchandise)

---

## 1. Background and Current State

Mapúa University’s MTO merchandise system has a complete backend with repositories, services, and REST API routers. The frontend (Next.js App Router) currently uses a mix of:

- Server components that already call the backend DAL (e.g., `app/admin/page.tsx` uses `getDashboardSummary()` from `frontend/lib/dal/dashboard.ts`).
- Client-side stores and mock data for some flows (e.g., `frontend/lib/orders-store.ts`, `frontend/lib/admin-store.ts`, `frontend/lib/mock-data.ts`).
- A client component `OrdersTable` that invokes network mutations from the browser, which we want to move to server actions.

This PRD defines a comprehensive plan to remove mock usage and integrate the UI with backend endpoints while adopting Next.js RSC, Suspense, and server actions.

References (existing specs to align with):
- `specs/api_endpionts_implementation.md`
- `specs/service_layer_implementation.md`
- `specs/repository_layer_implementation.md`

---

## 2. Objectives and Success Criteria

- Replace mock data with real backend endpoints across all relevant pages.
- Ensure mutations (start production, mark ready, delete, update status, create order) run as server actions, not in the client.
- Prefer RSC + Suspense for data loading. Avoid fetching from the client when possible.
- Maintain response validation with Zod at the DAL layer.
- Keep URL/state refresh behavior predictable with `router.refresh()` or `revalidatePath()` after server actions.

Acceptance (high level):
- All mock-based pages transitioned to backend-powered pages.
- Client components no longer perform direct API calls; mutations are server-side.
- No regressions in data displayed or workflows.

---

## 3. Inventory: Frontend Data Sources and Backends

Frontend key files (relevant):
- Orders admin list (RSC + Client table): `frontend/app/admin/orders/page.tsx` (RSC) → `OrdersTable` client component at `frontend/components/admin/orders-table.tsx`.
- Dashboard (RSC): `frontend/app/admin/page.tsx` (uses `getDashboardSummary`) → OK.
- Customer orders (Client + mock): `frontend/app/orders/page.tsx` uses `useOrdersStore` and `mockCustomer`/`mockProducts`.
- Stores and mock:
  - `frontend/lib/orders-store.ts` (persists mock orders, production, delivery, billing)
  - `frontend/lib/admin-store.ts` (mutates mock state, uses `mockProducts`)
  - `frontend/lib/mock-data.ts`
- DAL (already calling backend):
  - `frontend/lib/dal/orders.ts` (GET orders, GET detail, PATCH status, DELETE order, POST/ PATCH production)
  - `frontend/lib/dal/products.ts` (GET products, GET by id)
  - `frontend/lib/dal/dashboard.ts` (GET summary)

Backend routers (implemented):
- `backend/app/api/orders.py`
- `backend/app/api/production_orders.py`
- `backend/app/api/deliveries.py`
- `backend/app/api/billings.py`
- `backend/app/api/products.py`
- `backend/app/api/dashboard.py`

Schemas (examples):
- `backend/app/schemas/orders.py` (`OrderSummaryResponse` etc.)
- `backend/app/models.py` (status enums and models)
- `backend/app/services/order_service.py` (business workflows)

---

## 4. Gap Analysis: Frontend Mock vs. Backend Responses/Services

- Orders list (Admin):
  - Frontend `OrderSummarySchema` expects `created_at?: Date` (optional), see `frontend/lib/dal/orders.ts`.
  - Backend `OrderSummaryResponse` currently omits `created_at` (see `backend/app/schemas/orders.py` lines 69–76), but service returns it.
  - FastAPI will filter unknown fields based on the response model, so `created_at` may be dropped. UI uses `created_at` (shows date in `OrdersTable`).
  - Gap: Include `created_at` in `OrderSummaryResponse` to guarantee presence.

- Customer orders page (Customer-facing):
  - Currently uses mock store: `frontend/app/orders/page.tsx` and `frontend/lib/orders-store.ts`.
  - No per-customer filter on `GET /api/orders` (only `status` param). Customer view needs customer-scoped results.
  - Gap: Add `customer_id` (and optional `search`) to `GET /api/orders` or add a dedicated endpoint to fetch orders for the current customer. Alternatively, integrate auth and infer current customer on the backend.

- Admin actions from client (`OrdersTable`):
  - `OrdersTable` is a client component that calls DAL functions (`startProduction`, `markProductionInProgress`, `completeProductionOrder`, `getOrderDetail`) from the browser.
  - Gap: Mutations should be server actions to avoid client-side fetching and keep secrets/server runtime on the server.

- Public env exposure:
  - DAL uses `NEXT_PUBLIC_API_URL` resulting in client visibility when used in client components.
  - Gap: Use server-only env (e.g., `BACKEND_API_URL`) and keep all network calls in server context (RSC/server actions). Client components should call server actions, not the backend URL.

- Mock data/stores lingering:
  - `frontend/lib/mock-data.ts`, `frontend/lib/orders-store.ts`, `frontend/lib/admin-store.ts` drive significant UI behavior.
  - Gap: Replace with backend-driven data + server actions; deprecate/remove mock modules.

- Filtering/search:
  - Admin orders page supports client-side filtering by search term. Backend supports `status` filter.
  - Gap: Consider adding search parameters to API for server-side filtering (optional, phase 2). For now, RSC can fetch all orders and filter in-memory.

---

## 5. Backend Changes to Close Gaps

- Orders summary schema should expose `created_at`:
  - File: `backend/app/schemas/orders.py`
  - Update `OrderSummaryResponse` to include `created_at: datetime`.

- Add customer filter for orders:
  - File: `backend/app/api/orders.py` and `backend/app/services/order_service.py`.
  - Accept `customer_id: int | None` and optional `search: str | None` in `GET /api/orders`.
  - In `order_service.get_customer_orders`, add filters: by `customer_id` and (optional) name/id search.

- Optional: Align “recent orders” shape with frontend RSC typing (already aligned through `dashboard_service`).

- Error model consistency:
  - Ensure routers continue returning `SuccessResponse[T]` and appropriate errors per `specs/api_endpionts_implementation.md`.

Non-goals for this PRD:
- AuthN/AuthZ. For customer scoping, we’ll either pass `customer_id` explicitly or stub until auth is added.

---

## 6. Frontend Changes to Close Gaps (RSC, Suspense, Server Actions)

- Environment separation:
  - Introduce server-only `BACKEND_API_URL` (not exposed via NEXT_PUBLIC) for server actions and RSC.
  - Ensure DAL modules with network calls are used only in server files (RSC/pages or server actions). For client components, expose server actions instead of DAL functions.

- Orders Admin (RSC + Client table):
  - File: `frontend/app/admin/orders/page.tsx` remains an RSC that calls `getOrders()`.
  - Migrate `OrdersTable` mutations to server actions:
    - Create `frontend/app/admin/orders/actions.ts` with server actions:
      - `startProductionAction(orderId: number)`
      - `markOrderReadyAction(orderId: number)` (may call `markProductionInProgressAction` + `completeProductionAction` under the hood, or the production service endpoints in sequence)
      - `updateOrderStatusAction(orderId: number, status: SalesOrderStatus)`
      - `deleteOrderAction(orderId: number)`
    - Each action will call backend via DAL on the server and `revalidatePath("/admin/orders")`.
  - Update `frontend/components/admin/orders-table.tsx` to submit small forms (or `useFormStatus`) to these server actions instead of calling DAL from client code. Keep optimistic UI optional.
  - Add Suspense:
    - Wrap the orders table in a Suspense boundary via RSC parent.
    - Provide `app/admin/orders/loading.tsx` for skeletons.

- Customer Orders (RSC):
  - Replace `frontend/app/orders/page.tsx` (client with mock) with an RSC that fetches from backend:
    - Add `getOrders({ customer_id })` support (after backend change) and render real data.
    - Provide `app/orders/loading.tsx` for Suspense.
  - If user identity is not implemented, pass `customer_id` from a placeholder or route param until auth exists.

- Deprecate mock stores:
  - Remove usage of `frontend/lib/orders-store.ts`, `frontend/lib/admin-store.ts`, and `frontend/lib/mock-data.ts` from pages/components.
  - Retain files temporarily behind a feature flag or delete in a follow-up PR after migration is stable.

- DAL hygiene:
  - Keep `frontend/lib/dal/orders.ts`/`products.ts`/`dashboard.ts` as server-only consumers.
  - If any DAL function must be callable from client, wrap it in a server action instead.

---

## 7. Data Mapping (Backend → UI)

- Orders list (Admin):
  - Backend (`OrderSummaryResponse` after change): `{ id, customer_name, status, total_amount, created_at }`
  - UI (`OrdersTable` rows): `id`, `customer_name`, `new Date(created_at).toLocaleDateString()`, `total_amount`, `status` as badge.

- Order detail (Admin actions rely on it):
  - Backend `OrderDetailResponse`: `{ id, customer_id, customer_name, status, total_amount, created_at, items[], production_orders[], deliveries[], billing? }`
  - UI needs `production_orders` to compute active / latest production order when marking ready.

- Dashboard summary:
  - Backend `GET /api/dashboard/summary` matches DAL `DashboardSummaryResponseSchema` usage in `app/admin/page.tsx`.

---

## 8. Detailed Implementation Plan

Phase 1 — Backend gaps (small, safe):
- Add `created_at` to `OrderSummaryResponse` in `backend/app/schemas/orders.py`.
- Extend `GET /api/orders` to support `customer_id` (and optional `search`). Thread param to `order_service.get_customer_orders`.
- Update tests under `backend/tests/` accordingly.

Phase 2 — Frontend server actions and RSC:
- Create `frontend/app/admin/orders/actions.ts` with server actions (using DAL). For each action:
  - Validate input → call DAL → handle errors → `revalidatePath("/admin/orders")` → return message.
- Update `frontend/components/admin/orders-table.tsx`:
  - Replace `onClick` handlers with `<form action={startProductionAction}>`/`<form action={markOrderReadyAction}>` patterns or a single action with a discriminator.
  - Remove direct DAL calls from client. Keep router refresh.
- Add Suspense fallbacks:
  - `frontend/app/admin/orders/loading.tsx`
  - `frontend/app/orders/loading.tsx`

Phase 3 — Replace customer mock orders with backend:
- Rewrite `frontend/app/orders/page.tsx` as an RSC (remove `"use client"`).
- Fetch orders via `getOrders({ customer_id })` and render items (product names may require joining—use `product_name` from order detail when needed or keep a minimal list view).
- Remove usage of `mockCustomer`, `mockProducts` in that page.

Phase 4 — Cleanup:
- Remove references to `frontend/lib/orders-store.ts`, `frontend/lib/admin-store.ts`, and `frontend/lib/mock-data.ts`.
- Optionally delete files after a stabilization period.

---

## 9. Error Handling, Loading States, and UX

- Use try/catch in RSC to set `error` strings passed to client components.
- Provide `loading.tsx` skeletons for orders/admin pages.
- In server actions, surface meaningful error messages (e.g., InvalidTransitionError) and log for debugging.
- Keep client-side optimistic UI optional; server is source of truth.

---

## 10. Security and Configuration

- Replace `NEXT_PUBLIC_API_URL` usage for mutations with server-only `BACKEND_API_URL` in server actions and RSC.
- Ensure DAL functions that are used in actions/pages are only imported on the server.

---

## 11. Testing Plan

- Unit: Update backend tests for `GET /api/orders` to cover `customer_id` and presence of `created_at`.
- Integration (frontend):
  - Admin orders page renders server data and action flows transition statuses (Created → In Production → Ready for Delivery).
  - Customer orders page shows real orders for a given `customer_id`.
- E2E (manual or Playwright): common flows succeed without mock data.

---

## 12. Acceptance Criteria (Detailed)

- Admin orders list shows real orders with correct `created_at`.
- Buttons “Start Production” and “Mark Ready” execute via server actions; network calls are server-side.
- Customer orders page is an RSC, no `"use client"`, no mock imports.
- No remaining imports of `frontend/lib/mock-data.ts`, `frontend/lib/orders-store.ts`, `frontend/lib/admin-store.ts` in pages/components.
- Suspense fallbacks (`loading.tsx`) present for admin orders and customer orders.

---

## 13. Rollout and Migration

- Ship backend schema/endpoint changes first.
- Merge frontend server actions & RSC rewrites next.
- Feature-flag removal of mock modules for fast rollback if needed.

---

## 14. Future Enhancements

- Add AuthN and infer `customer_id` on backend; drop explicit param from UI.
- Add server-side search/sort/pagination as data grows.
- Convert more UI segments to stream via Suspense for faster TTFB.
- Add WebSocket/SSE for live status updates.

---

## 15. References to Existing Specs (Traceability)

- API contracts and response wrappers: `specs/api_endpionts_implementation.md`
- Service orchestration and allowed transitions: `specs/service_layer_implementation.md`
- Repository patterns and exception mapping: `specs/repository_layer_implementation.md`

This PRD aligns with those documents’ structure (goals, design principles, endpoints, implementation plan, acceptance criteria) and focuses on frontend integration plus minor backend adjustments required for a complete mock-to-API migration.
