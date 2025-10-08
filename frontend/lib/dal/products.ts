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
 * Zod schema for Product creation request
 */
export const ProductCreateRequestSchema = z.object({
  name: z.string().min(1, "Product name is required"),
  description: z.string().min(1, "Product description is required"),
  price: z.number().min(0.01, "Price must be greater than 0"),
  stock_qty: z.number().min(0, "Stock quantity must be 0 or greater").default(0),
  image_url: z.string().url("Invalid image URL").optional().or(z.literal(""))
})

/**
 * Zod schema for Product update request
 */
export const ProductUpdateRequestSchema = z.object({
  name: z.string().min(1, "Product name is required"),
  description: z.string().min(1, "Product description is required"),
  price: z.number().min(0.01, "Price must be greater than 0"),
  stock_qty: z.number().min(0, "Stock quantity must be 0 or greater"),
  image_url: z.string().url("Invalid image URL").optional().or(z.literal(""))
})
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


/**
 * Create a new product
 * @param productData - Product data to create
 * @returns Promise resolving to the created product
 * @throws Error if API request fails or returns invalid response
 */
export async function createProduct(productData: {
  name: string
  description: string
  price: number
  stock_qty?: number
  image_url?: string
}): Promise<Product> {
  try {
    // Validate the input data using Zod
    const validatedData = ProductCreateRequestSchema.parse(productData)

    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL
    if (!baseUrl) {
      throw new Error("BACKEND_API_URL or NEXT_PUBLIC_API_URL is not configured")
    }

    const response = await fetch(`${baseUrl}/api/products`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(validatedData),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
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
      console.error('Product creation validation failed:', error.errors)
      throw new Error(`Invalid product data: ${error.message}`)
    }

    console.error('Failed to create product:', error)
    throw new Error(`Failed to create product: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}

/**
 * Update an existing product
 * @param productId - The product ID to update
 * @param productData - Updated product data
 * @returns Promise resolving to the updated product
 * @throws Error if API request fails or returns invalid response
 */
export async function updateProduct(productId: number, productData: {
  name: string
  description: string
  price: number
  stock_qty: number
  image_url?: string
}): Promise<Product> {
  try {
    // Validate the input data using Zod
    const validatedData = ProductUpdateRequestSchema.parse(productData)

    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL
    if (!baseUrl) {
      throw new Error("BACKEND_API_URL or NEXT_PUBLIC_API_URL is not configured")
    }

    const response = await fetch(`${baseUrl}/api/products/${productId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(validatedData),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      if (response.status === 404) {
        throw new Error(`Product with ID ${productId} not found`)
      }
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
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
      console.error('Product update validation failed:', error.errors)
      throw new Error(`Invalid product data: ${error.message}`)
    }

    console.error('Failed to update product:', error)
    throw new Error(`Failed to update product: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}


/**
 * Delete a product by ID
 * @param productId - The product ID to delete
 * @returns Promise resolving to void
 * @throws Error if API request fails or product not found
 */
export async function deleteProduct(productId: number): Promise<void> {
  try {
    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL
    if (!baseUrl) {
      throw new Error("BACKEND_API_URL or NEXT_PUBLIC_API_URL is not configured")
    }

    const response = await fetch(`${baseUrl}/api/products/${productId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error(`Product with ID ${productId} not found`)
      }
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }

    // No response body expected for DELETE
  } catch (error) {
    console.error(`Failed to delete product ${productId}:`, error)
    throw new Error(`Failed to delete product: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}
