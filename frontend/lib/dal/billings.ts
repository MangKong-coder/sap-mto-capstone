/**
 * Billings Data Access Layer
 * Handles API requests, response validation, and data transformation for billings
 */

import { z } from 'zod'
import { ApiResponseSchema } from '../schema/api-response'

/**
 * Zod schema for Billing validation
 */
export const BillingSchema = z.object({
  id: z.number(),
  sales_order_id: z.number(),
  invoice_number: z.string().nullable(),
  amount: z.number(),
  billed_date: z.coerce.date().nullable(),
})

export type Billing = z.infer<typeof BillingSchema>

/**
 * Zod schema for CreateBillingRequest validation
 */
export const CreateBillingRequestSchema = z.object({
  sales_order_id: z.number(),
})

export type CreateBillingRequest = z.infer<typeof CreateBillingRequestSchema>

/**
 * Zod schema for SendInvoiceRequest validation
 */
export const SendInvoiceRequestSchema = z.object({
  sales_order_id: z.number(),
})

export type SendInvoiceRequest = z.infer<typeof SendInvoiceRequestSchema>

const API_BASE = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL

function assertApiBase(): string {
  if (!API_BASE) {
    throw new Error("BACKEND_API_URL or NEXT_PUBLIC_API_URL is not configured")
  }
  return API_BASE
}

/**
 * Fetch all billings from the API
 * @returns Promise resolving to array of billings
 * @throws Error if API request fails or returns invalid response
 */
export async function getBillings(fetchOptions: RequestInit = {}): Promise<Billing[]> {
  try {
    const response = await fetch(`${assertApiBase()}/api/billings`, {
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
    const apiResponseSchema = ApiResponseSchema(z.array(BillingSchema))
    const apiResponse = apiResponseSchema.parse(rawData)

    return apiResponse.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error("Failed to fetch billings:", error)
    throw new Error(`Failed to load billings: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

/**
 * Create a new billing for a sales order
 * @param salesOrderId - The sales order ID to create billing for
 * @returns Promise resolving to the created billing
 * @throws Error if API request fails or returns invalid response
 */
export async function createBilling(salesOrderId: number, fetchOptions: RequestInit = {}): Promise<Billing> {
  try {
    const response = await fetch(`${assertApiBase()}/api/billings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...fetchOptions.headers,
      },
      body: JSON.stringify({ sales_order_id: salesOrderId }),
      ...fetchOptions,
    })

    if (!response.ok) {
      const detail = await response.json().catch(() => null)
      throw new Error(detail?.detail ?? `HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()

    // Validate the API response structure using Zod
    const apiResponseSchema = ApiResponseSchema(BillingSchema)
    const apiResponse = apiResponseSchema.parse(rawData)

    return apiResponse.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error(`Failed to create billing for sales order ${salesOrderId}:`, error)
    throw new Error(`Failed to create billing: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

/**
 * Create a billing and send invoice email for a sales order
 * @param salesOrderId - The sales order ID to create billing for and send invoice
 * @returns Promise resolving to the created billing
 * @throws Error if API request fails or returns invalid response
 */
export async function sendInvoice(salesOrderId: number, fetchOptions: RequestInit = {}): Promise<Billing> {
  try {
    const response = await fetch(`${assertApiBase()}/api/billings/send-invoice`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...fetchOptions.headers,
      },
      body: JSON.stringify({ sales_order_id: salesOrderId }),
      ...fetchOptions,
    })

    if (!response.ok) {
      const detail = await response.json().catch(() => null)
      throw new Error(detail?.detail ?? `HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()

    // Validate the API response structure using Zod
    const apiResponseSchema = ApiResponseSchema(BillingSchema)
    const apiResponse = apiResponseSchema.parse(rawData)

    return apiResponse.data
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error("API response validation failed:", error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error(`Failed to send invoice for sales order ${salesOrderId}:`, error)
    throw new Error(`Failed to send invoice: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}
