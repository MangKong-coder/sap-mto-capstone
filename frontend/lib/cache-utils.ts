/**
 * Cache Utilities
 * Helper functions for managing Next.js cache invalidation
 */

import { revalidatePath, revalidateTag } from "next/cache"

/**
 * Revalidates all order-related cache entries
 * Use this after any mutation that affects order data
 * 
 * @param orderId - Optional specific order ID to revalidate. If omitted, only list caches are revalidated
 */
export function revalidateOrders(orderId?: number) {
  // Revalidate cache tags used in fetch requests
  revalidateTag('orders-list')
  revalidateTag('orders')
  
  if (orderId !== undefined) {
    revalidateTag(`order-${orderId}`)
  }
  
  // Revalidate route caches
  revalidatePath('/orders')
  revalidatePath('/admin/orders')
  
  if (orderId !== undefined) {
    revalidatePath(`/orders/${orderId}`)
  }
}

/**
 * Cache tags used in the application
 * Keep this in sync with tags used in DAL functions
 */
export const CACHE_TAGS = {
  ORDERS_LIST: 'orders-list',
  ORDERS: 'orders',
  ORDER: (id: number) => `order-${id}`,
  WORK_CENTERS: 'work-centers',
} as const

/**
 * Route paths that need revalidation
 */
export const CACHE_PATHS = {
  ORDERS: '/orders',
  ADMIN_ORDERS: '/admin/orders',
  ORDER_DETAIL: (id: number) => `/orders/${id}`,
} as const
