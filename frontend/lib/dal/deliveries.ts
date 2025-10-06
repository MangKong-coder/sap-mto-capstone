/**
 * Deliveries Data Access Layer
 * Handles API requests, response validation, and data transformation for deliveries
 */

import { z } from 'zod'
import { ApiResponseSchema } from '../schema/api-response'

/**
 * Zod schema for Delivery validation
 */
export const DeliverySchema = z.object({
  id: z.number(),
  sales_order_id: z.number(),
  delivery_date: z.coerce.date().nullable(),
  status: z.string(),
})

export type Delivery = z.infer<typeof DeliverySchema>

/**
 * Zod schema for UpdateDeliveryStatusRequest validation
 */
export const UpdateDeliveryStatusRequestSchema = z.object({
  status: z.string(),
})

export type UpdateDeliveryStatusRequest = z.infer<typeof UpdateDeliveryStatusRequestSchema>

const API_BASE = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL

function assertApiBase(): string {
  if (!API_BASE) {
    throw new Error("BACKEND_API_URL or NEXT_PUBLIC_API_URL is not configured")
  }
  return API_BASE
}

/**
 * Fetch all deliveries from the API
 * @returns Promise resolving to array of deliveries
 * @throws Error if API request fails or returns invalid response
 */
export async function getDeliveries(fetchOptions: RequestInit = {}): Promise<Delivery[]> {
  try {
    const response = await fetch(`${assertApiBase()}/api/deliveries`, {
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
    const apiResponseSchema = ApiResponseSchema(z.array(DeliverySchema))
    const apiResponse = apiResponseSchema.parse(rawData)

    return apiResponse.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error("Failed to fetch deliveries:", error)
    throw new Error(`Failed to load deliveries: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

/**
 * Update delivery status
 * @param deliveryId - The delivery ID to update
 * @param status - The new status for the delivery
 * @returns Promise resolving to the updated delivery
 * @throws Error if API request fails or returns invalid response
 */
export async function updateDeliveryStatus(deliveryId: number, status: string, fetchOptions: RequestInit = {}): Promise<Delivery> {
  try {
    const response = await fetch(`${assertApiBase()}/api/deliveries/${deliveryId}/status`, {
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
    const apiResponseSchema = ApiResponseSchema(DeliverySchema)
    const apiResponse = apiResponseSchema.parse(rawData)

    return apiResponse.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error(`Failed to update delivery ${deliveryId} status:`, error)
    throw new Error(`Failed to update delivery status: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}
