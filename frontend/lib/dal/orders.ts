/**
 * Orders Data Access Layer
 * Provides typed helpers for interacting with sales orders endpoints.
 */

import { z } from "zod"

import { ApiResponseSchema } from "../schema/api-response"
import { SalesOrderStatus } from "../types"

export const OrderSummarySchema = z.object({
  id: z.number(),
  customer_name: z.string().nullable(),
  status: z.nativeEnum(SalesOrderStatus),
  total_amount: z.number(),
  created_at: z.coerce.date().optional(),
})

const OrderListResponseSchema = ApiResponseSchema(z.array(OrderSummarySchema))

export const OrderDetailSchema = z.object({
  id: z.number(),
  customer_id: z.number(),
  customer_name: z.string().nullable(),
  status: z.nativeEnum(SalesOrderStatus),
  total_amount: z.number(),
  created_at: z.coerce.date(),
  items: z.array(
    z.object({
      id: z.number(),
      product_id: z.number(),
      product_name: z.string().nullable(),
      quantity: z.number(),
      subtotal: z.number(),
    }),
  ),
  production_orders: z.array(
    z.object({
      id: z.number(),
      status: z.string(),
      start_date: z.coerce.date().nullable(),
      end_date: z.coerce.date().nullable(),
    }),
  ),
  deliveries: z.array(
    z.object({
      id: z.number(),
      status: z.string(),
      delivery_date: z.coerce.date().nullable(),
    }),
  ),
  billing: z
    .object({
      id: z.number(),
      invoice_number: z.string().nullable(),
      amount: z.number(),
      billed_date: z.coerce.date().nullable(),
    })
    .nullable(),
})

const OrderDetailResponseSchema = ApiResponseSchema(OrderDetailSchema)

const OrderItemPayloadSchema = z.object({
  product_id: z.number(),
  quantity: z.number().min(1, "Quantity must be at least 1"),
})

const OrderCreateRequestSchema = z.object({
  customer_id: z.number(),
  items: z.array(OrderItemPayloadSchema),
})

const OrderCreateResponseSchema = ApiResponseSchema(OrderDetailSchema)

const ProductionOrderSchema = z.object({
  id: z.number(),
  sales_order_id: z.number(),
  status: z.string(),
  start_date: z.coerce.date().nullable(),
  end_date: z.coerce.date().nullable(),
})

const ProductionOrderResponseSchema = ApiResponseSchema(ProductionOrderSchema)

export type OrderSummary = z.infer<typeof OrderSummarySchema>
export type OrderDetail = z.infer<typeof OrderDetailSchema>
export type ProductionOrder = z.infer<typeof ProductionOrderSchema>

function buildHeaders(base: HeadersInit | undefined, overrides: Record<string, string>): Headers {
  const headers = new Headers(overrides)
  if (!base) {
    return headers
  }

  const provided = base instanceof Headers ? base : new Headers(base)
  provided.forEach((value, key) => {
    headers.set(key, value)
  })

  return headers
}

const API_BASE = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL

function assertApiBase(): string {
  if (!API_BASE) {
    throw new Error("BACKEND_API_URL or NEXT_PUBLIC_API_URL is not configured")
  }
  return API_BASE
}

export async function getOrders(
  fetchOptions: RequestInit = {},
  params?: {
    status?: string
    customer_id?: number
  }
): Promise<OrderSummary[]> {
  try {
    const searchParams = new URLSearchParams()

    if (params?.status) {
      searchParams.append("status", params.status)
    }

    if (params?.customer_id) {
      searchParams.append("customer_id", params.customer_id.toString())
    }

    const url = `${assertApiBase()}/api/orders${searchParams.toString() ? `?${searchParams.toString()}` : ""}`

    const response = await fetch(url, {
      // Use ISR-friendly caching for build-time generation
      next: { revalidate: 300, tags: ['orders-list'] },
      ...fetchOptions,
      method: fetchOptions.method ?? "GET",
      headers: buildHeaders(fetchOptions.headers, {
        "Content-Type": "application/json",
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()
    const parsed = OrderListResponseSchema.parse(rawData)

    return parsed.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error("Failed to fetch orders:", error)
    throw new Error(`Failed to load orders: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

export async function updateOrderStatus(orderId: number, status: SalesOrderStatus): Promise<OrderDetail> {
  try {
    const response = await fetch(`${assertApiBase()}/api/orders/${orderId}/status`, {
      method: "PATCH",
      headers: buildHeaders(undefined, {
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({ status }),
    })

    if (!response.ok) {
      const detail = await response.json().catch(() => null)
      throw new Error(detail?.detail ?? `HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()
    const parsed = OrderDetailResponseSchema.parse(rawData)

    return parsed.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error(`Failed to update order ${orderId} status:`, error)
    throw new Error(`Failed to update order: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

export async function deleteOrder(orderId: number): Promise<void> {
  const response = await fetch(`${assertApiBase()}/api/orders/${orderId}`, {
    method: "DELETE",
    headers: buildHeaders(undefined, {
      "Content-Type": "application/json",
    }),
  })

  if (!response.ok) {
    const detail = await response.json().catch(() => null)
    throw new Error(detail?.detail ?? `HTTP error! status: ${response.status}`)
  }
}

export async function getOrderDetail(orderId: number): Promise<OrderDetail> {
  try {
    const response = await fetch(`${assertApiBase()}/api/orders/${orderId}`, {
      method: "GET",
      headers: buildHeaders(undefined, {
        "Content-Type": "application/json",
      }),
      // Use ISR-friendly caching instead of no-store
      next: { revalidate: 300, tags: [`order-${orderId}`, 'orders'] }
    })

    if (!response.ok) {
      const detail = await response.json().catch(() => null)
      throw new Error(detail?.detail ?? `HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()
    const parsed = OrderDetailResponseSchema.parse(rawData)

    return parsed.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error(`Failed to fetch order ${orderId}:`, error)
    throw new Error(`Failed to load order: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

export async function startProduction(orderId: number): Promise<ProductionOrder> {
  try {
    const response = await fetch(`${assertApiBase()}/api/production-orders`, {
      method: "POST",
      headers: buildHeaders(undefined, {
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({ sales_order_id: orderId }),
    })

    if (!response.ok) {
      const detail = await response.json().catch(() => null)
      throw new Error(detail?.detail ?? `HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()
    const parsed = ProductionOrderResponseSchema.parse(rawData)

    return parsed.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error(`Failed to start production for order ${orderId}:`, error)
    throw new Error(`Failed to start production: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

export async function markProductionInProgress(productionId: number): Promise<ProductionOrder> {
  try {
    const response = await fetch(`${assertApiBase()}/api/production-orders/${productionId}/start`, {
      method: "PATCH",
      headers: buildHeaders(undefined, {
        "Content-Type": "application/json",
      }),
    })

    if (!response.ok) {
      const detail = await response.json().catch(() => null)
      throw new Error(detail?.detail ?? `HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()
    const parsed = ProductionOrderResponseSchema.parse(rawData)

    return parsed.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error(`Failed to mark production ${productionId} in progress:`, error)
    throw new Error(`Failed to update production order: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

export async function completeProductionOrder(productionId: number): Promise<ProductionOrder> {
  try {
    const response = await fetch(`${assertApiBase()}/api/production-orders/${productionId}/complete`, {
      method: "PATCH",
      headers: buildHeaders(undefined, {
        "Content-Type": "application/json",
      }),
    })

    if (!response.ok) {
      const detail = await response.json().catch(() => null)
      throw new Error(detail?.detail ?? `HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()
    const parsed = ProductionOrderResponseSchema.parse(rawData)

    return parsed.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error(`Failed to complete production ${productionId}:`, error)
    throw new Error(`Failed to complete production order: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}


export async function createOrder(
  customerId: number,
  items: Array<{ product_id: number; quantity: number }>
): Promise<OrderDetail> {
  try {
    // Validate the input data using Zod
    const validatedData = OrderCreateRequestSchema.parse({
      customer_id: customerId,
      items: items,
    })

    const response = await fetch(`${assertApiBase()}/api/orders`, {
      method: "POST",
      headers: buildHeaders(undefined, {
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(validatedData),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()
    const parsed = OrderCreateResponseSchema.parse(rawData)

    return parsed.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("Order creation validation failed:", error.errors)
      throw new Error(`Invalid order data: ${error.message}`)
    }

    console.error("Failed to create order:", error)
    throw new Error(`Failed to create order: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}
