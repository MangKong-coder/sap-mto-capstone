/**
 * Production Orders Data Access Layer
 * Handles API requests, response validation, and data transformation for production orders
 */

import { z } from 'zod'
import { ApiResponseSchema } from '../schema/api-response'

/**
 * Zod schema for ProductionOrder validation
 */
export const ProductionOrderSchema = z.object({
  id: z.number(),
  sales_order_id: z.number(),
  status: z.string(),
  start_date: z.coerce.date().nullable(),
  end_date: z.coerce.date().nullable(),
})

export type ProductionOrder = z.infer<typeof ProductionOrderSchema>

/**
 * Zod schema for UpdateProductionStatusRequest validation
 */
export const UpdateProductionStatusRequestSchema = z.object({
  status: z.string(),
})

export type UpdateProductionStatusRequest = z.infer<typeof UpdateProductionStatusRequestSchema>

const API_BASE = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL

function assertApiBase(): string {
  if (!API_BASE) {
    throw new Error("BACKEND_API_URL or NEXT_PUBLIC_API_URL is not configured")
  }
  return API_BASE
}

/**
 * Fetch all production orders from the API
 * @returns Promise resolving to array of production orders
 * @throws Error if API request fails or returns invalid response
 */
export async function getProductionOrders(fetchOptions: RequestInit = {}): Promise<ProductionOrder[]> {
  try {
    const response = await fetch(`${assertApiBase()}/api/production-orders`, {
      cache: "no-store",
      ...fetchOptions,
      method: fetchOptions.method ?? "GET",
      headers: {
        "Content-Type": "application/json",
        ...fetchOptions.headers,
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()

    // Validate the API response structure using Zod
    const apiResponseSchema = ApiResponseSchema(z.array(ProductionOrderSchema))
    const apiResponse = apiResponseSchema.parse(rawData)

    return apiResponse.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error("Failed to fetch production orders:", error)
    throw new Error(`Failed to load production orders: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

/**
 * Update production order status
 * @param productionId - The production order ID to update
 * @param status - The new status for the production order
 * @returns Promise resolving to the updated production order
 * @throws Error if API request fails or returns invalid response
 */
export async function updateProductionStatus(productionId: number, status: string, fetchOptions: RequestInit = {}): Promise<ProductionOrder> {
  try {
    const response = await fetch(`${assertApiBase()}/api/production-orders/${productionId}/status`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        ...fetchOptions.headers,
      },
      body: JSON.stringify({ status }),
      ...fetchOptions,
    })

    if (!response.ok) {
      const detail = await response.json().catch(() => null)
      throw new Error(detail?.detail ?? `HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()

    // Validate the API response structure using Zod
    const apiResponseSchema = ApiResponseSchema(ProductionOrderSchema)
    const apiResponse = apiResponseSchema.parse(rawData)

    return apiResponse.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error(`Failed to update production order ${productionId} status:`, error)
    throw new Error(`Failed to update production order status: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}
