/**
 * Products Data Access Layer
 * Handles API requests, response validation, and data transformation for products
 */

import { z } from 'zod'
import { Product } from "@/lib/types"
import { ApiResponseSchema } from '../schema/api-response'

/**
 * Zod schema for API Response wrapper from backend
 */


/**
 * Zod schema for Product validation
 */
export const ProductSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string(),
  price: z.number(),
  stock_qty: z.number().nullable(),
  image_url: z.string().nullable()
})


/**
 * Fetch all products from the API
 * @param search - Optional search query to filter products by name
 * @returns Promise resolving to array of products
 * @throws Error if API request fails or returns invalid response
 */
export async function getProducts(search?: string): Promise<Product[]> {
  try {
    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL
    if (!baseUrl) {
      throw new Error("BACKEND_API_URL or NEXT_PUBLIC_API_URL is not configured")
    }

    const url = new URL(`${baseUrl}/api/products`)
    if (search) {
      url.searchParams.set('search', search)
    }

    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()

    // Validate the API response structure using Zod
    const apiResponseSchema = ApiResponseSchema(z.array(ProductSchema))
    const apiResponse = apiResponseSchema.parse(rawData)

    // Transform the validated data to match our Product interface
    const validatedProducts: Product[] = apiResponse.data.map((product) => ({
      id: product.id,
      name: product.name,
      description: product.description,
      price: product.price,
      stock_qty: product.stock_qty ?? 0, // Convert null to 0 for our interface
      image_url: product.image_url
    }))

    return validatedProducts
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error('API response validation failed:', error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error('Failed to fetch products:', error)
    throw new Error(`Failed to load products: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}


/**
 * Fetch a single product by ID
 * @param productId - The product ID to fetch
 * @returns Promise resolving to a single product
 * @throws Error if product not found or API request fails
 */
export async function getProductById(productId: number): Promise<Product> {
  try {
    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL
    if (!baseUrl) {
      throw new Error("BACKEND_API_URL or NEXT_PUBLIC_API_URL is not configured")
    }

    const response = await fetch(`${baseUrl}/api/products/${productId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error(`Product with ID ${productId} not found`)
      }
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const rawData = await response.json()

    // Validate the API response structure using Zod
    const apiResponseSchema = ApiResponseSchema(ProductSchema)
    const apiResponse = apiResponseSchema.parse(rawData)

    // Transform the validated data to match our Product interface
    const product: Product = {
      id: apiResponse.data.id,
      name: apiResponse.data.name,
      description: apiResponse.data.description,
      price: apiResponse.data.price,
      stock_qty: apiResponse.data.stock_qty ?? 0, // Convert null to 0 for our interface
      image_url: apiResponse.data.image_url
    }

    return product
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error('API response validation failed:', error.errors)
      throw new Error(`API returned invalid response format: ${error.message}`)
    }

    console.error(`Failed to fetch product ${productId}:`, error)
    throw new Error(`Failed to load product: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}
