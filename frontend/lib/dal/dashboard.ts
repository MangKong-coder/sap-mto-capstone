/**
 * Dashboard Data Access Layer
 * Handles API requests, response validation, and data transformation for dashboard
 */

import { z } from 'zod'
import { ApiResponseSchema } from '../schema/api-response'

/**
 * Zod schema for TopProductResponse validation
 */
export const TopProductResponseSchema = z.object({
  product_id: z.number(),
  name: z.string().nullable(),
  orders: z.number(),
})

/**
 * Zod schema for RecentOrderResponse validation
 */
export const RecentOrderResponseSchema = z.object({
  id: z.number(),
  customer_name: z.string(),
  status: z.string(),
  total_amount: z.number(),
  created_at: z.coerce.date(),
})

/**
 * Zod schema for DashboardSummaryResponse validation
 */
export const DashboardSummaryResponseSchema = z.object({
  total_orders: z.number(),
  in_production: z.number(),
  ready_for_delivery: z.number(),
  billed: z.number(),
  top_products: z.array(TopProductResponseSchema),
  recent_orders: z.array(RecentOrderResponseSchema),
})

export type DashboardSummaryResponse = z.infer<typeof DashboardSummaryResponseSchema>
export type TopProductResponse = z.infer<typeof TopProductResponseSchema>
export type RecentOrderResponse = z.infer<typeof RecentOrderResponseSchema>

/**
 * Fetch dashboard summary data from the API
 * @returns Promise resolving to dashboard summary data
 * @throws Error if API request fails or returns invalid response
 */
export async function getDashboardSummary(fetchOptions: RequestInit = {}): Promise<DashboardSummaryResponse> {
  try {
    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL
    if (!baseUrl) {
      throw new Error("BACKEND_API_URL or NEXT_PUBLIC_API_URL is not configured")
    }

    const headers = new Headers({
      'Content-Type': 'application/json',
    })

    if (fetchOptions.headers) {
      const providedHeaders =
        fetchOptions.headers instanceof Headers
          ? fetchOptions.headers
          : new Headers(fetchOptions.headers)

      providedHeaders.forEach((value, key) => {
        headers.set(key, value)
      })
    }

    const response = await fetch(`${baseUrl}/api/dashboard/summary`, {
      ...fetchOptions,
      method: fetchOptions.method ?? 'GET',
      headers,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()

    // Validate the API response structure using Zod
    const apiResponseSchema = ApiResponseSchema(DashboardSummaryResponseSchema)
    const apiResponse = apiResponseSchema.parse(rawData)

    return apiResponse.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error('API response validation failed:', error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error('Failed to fetch dashboard summary:', error)
    throw new Error(`Failed to load dashboard summary: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}
