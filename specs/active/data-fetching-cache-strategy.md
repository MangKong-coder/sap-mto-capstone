# Data Fetching & Cache Strategy

## Overview

This document describes the caching strategy implemented for data fetching in the frontend application, specifically for order data management.

## Problem Statement

The application was experiencing data inconsistencies across pages after mutations (create, update, delete operations). Specifically:

- When starting production on an order, the status didn't update on the current page or other pages
- When marking an order ready for delivery, the changes weren't reflected consistently
- Order list pages showed stale data after creating or deleting orders

### Root Cause

The issue was a **cache invalidation mismatch**:

1. **Data Access Layer (DAL)** functions used Next.js cache tags in fetch requests:
   - `getOrders()`: `tags: ['orders-list']`
   - `getOrderDetail(orderId)`: `tags: ['order-${orderId}', 'orders']`

2. **Server Actions** only used `revalidatePath()`, which invalidates the Full Route Cache but **NOT** the Data Cache tagged with those tags

3. Next.js has two separate cache layers:
   - **Data Cache**: Stores fetch request results, tagged with cache tags
   - **Full Route Cache**: Stores rendered route output

## Solution

### 1. Cache Tag Strategy

All DAL functions that fetch order data use consistent cache tags:

```typescript
// lib/dal/orders.ts
export async function getOrders() {
  const response = await fetch(url, {
    next: { revalidate: 300, tags: ['orders-list'] }
  })
}

export async function getOrderDetail(orderId: number) {
  const response = await fetch(url, {
    next: { revalidate: 300, tags: [`order-${orderId}`, 'orders'] }
  })
}
```

### 2. Cache Invalidation Helper

Created a reusable helper function in `lib/cache-utils.ts`:

```typescript
export function revalidateOrders(orderId?: number) {
  // Revalidate cache tags (Data Cache)
  revalidateTag('orders-list')
  revalidateTag('orders')
  
  if (orderId !== undefined) {
    revalidateTag(`order-${orderId}`)
  }
  
  // Revalidate route caches (Full Route Cache)
  revalidatePath('/orders')
  revalidatePath('/admin/orders')
  
  if (orderId !== undefined) {
    revalidatePath(`/orders/${orderId}`)
  }
}
```

### 3. Server Actions Update

All server actions now use the helper to invalidate both cache layers:

```typescript
// app/admin/orders/actions.ts
export async function startProductionAction(orderId: number) {
  try {
    await startProduction(orderId)
    revalidateOrders(orderId)  // Invalidates both Data Cache and Full Route Cache
    
    return { success: true, message: "Production started successfully" }
  } catch (error) {
    // Error handling...
  }
}
```

## Cache Layers in Next.js

### Data Cache
- Stores results from `fetch()` requests
- Tagged using `next: { tags: [...] }`
- Invalidated using `revalidateTag()`
- Persists across requests and deployments

### Full Route Cache
- Stores the rendered HTML/RSC payload for routes
- Invalidated using `revalidatePath()`
- Regenerated on next request after invalidation

### Why Both Are Needed

When a mutation occurs:
1. **`revalidateTag()`** marks the cached fetch data as stale, forcing fresh data fetches
2. **`revalidatePath()`** marks the rendered page as stale, forcing page re-rendering

Without both, you get:
- Stale data shown on pages (missing `revalidateTag`)
- Fresh data but old UI state (missing `revalidatePath`)

## Best Practices

### For DAL Functions

1. **Always tag fetch requests** for data that can be mutated:
```typescript
fetch(url, {
  next: { 
    revalidate: 300,  // Time-based revalidation (5 minutes)
    tags: ['resource-name']  // Tag for on-demand revalidation
  }
})
```

2. **Use consistent tag naming**:
   - List endpoints: `'resource-list'`
   - Detail endpoints: `['resource-${id}', 'resources']`
   - Related resources: Include parent tags

### For Server Actions

1. **Always revalidate after mutations**:
```typescript
export async function mutateResource(id: number) {
  await performMutation(id)
  revalidateResource(id)  // Use helper function
}
```

2. **Use the cache-utils helper** rather than manual invalidation

3. **Revalidate all affected resources**:
   - Direct resource
   - List views
   - Related resources

### Adding New Resources

When adding new resources with server-side caching:

1. **Define cache tags** in `lib/cache-utils.ts`:
```typescript
export const CACHE_TAGS = {
  RESOURCE_LIST: 'resource-list',
  RESOURCES: 'resources',
  RESOURCE: (id: number) => `resource-${id}`,
}
```

2. **Create a revalidation helper**:
```typescript
export function revalidateResources(resourceId?: number) {
  revalidateTag(CACHE_TAGS.RESOURCE_LIST)
  revalidateTag(CACHE_TAGS.RESOURCES)
  
  if (resourceId !== undefined) {
    revalidateTag(CACHE_TAGS.RESOURCE(resourceId))
    revalidatePath(`/resources/${resourceId}`)
  }
  
  revalidatePath('/resources')
}
```

3. **Use tags in DAL functions**:
```typescript
export async function getResources() {
  const response = await fetch(url, {
    next: { 
      revalidate: 300, 
      tags: [CACHE_TAGS.RESOURCE_LIST] 
    }
  })
}
```

4. **Use helper in server actions**:
```typescript
export async function createResourceAction(data: ResourceData) {
  const resource = await createResource(data)
  revalidateResources(resource.id)
  return resource
}
```

## Testing Cache Invalidation

To verify cache invalidation works correctly:

1. **Perform a mutation** (e.g., start production)
2. **Check the affected page** - data should update immediately
3. **Check related pages** (list views, detail views) - all should show updated data
4. **Check admin and user views** - both should reflect changes

If data is stale:
- Check if the DAL function uses cache tags
- Check if the server action calls the appropriate revalidation helper
- Verify tag names match between DAL and cache-utils

## References

- [Next.js Caching Documentation](https://nextjs.org/docs/app/building-your-application/caching)
- [Next.js Data Cache](https://nextjs.org/docs/app/building-your-application/caching#data-cache)
- [revalidateTag API](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)
- [revalidatePath API](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)

## Related Files

- `lib/dal/orders.ts` - Order data access layer with cache tags
- `lib/cache-utils.ts` - Cache invalidation helpers and constants
- `app/admin/orders/actions.ts` - Admin server actions
- `app/orders/actions.ts` - User-facing server actions
