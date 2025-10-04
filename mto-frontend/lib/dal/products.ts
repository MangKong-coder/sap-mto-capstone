/**
 * Data Access Layer for Products
 * 
 * This module provides functions to interact with the backend API
 * for product-related operations.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export interface Product {
  id: number
  sku: string
  name: string
  description?: string
  price: number
  created_at: string
  updated_at: string
}

export interface ProductCreate {
  sku: string
  name: string
  description?: string
  price: number
}

/**
 * Fetch products from the backend
 */
export async function getProducts(page: number = 1, size: number = 20): Promise<Product[]> {
  try {
    const response = await fetch(`${API_BASE}/products?page=${page}&size=${size}`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.status} ${response.statusText}`)
    }
    
    const products = await response.json()
    return products
  } catch (error) {
    console.error('Error fetching products:', error)
    throw new Error('Failed to fetch products')
  }
}

/**
 * Fetch a single product by ID
 */
export async function getProductById(productId: number): Promise<Product> {
  try {
    const response = await fetch(`${API_BASE}/products/${productId}`)
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Product not found')
      }
      throw new Error(`Failed to fetch product: ${response.status} ${response.statusText}`)
    }
    
    const product = await response.json()
    return product
  } catch (error) {
    console.error('Error fetching product:', error)
    throw error
  }
}

/**
 * Fetch a product by SKU
 */
export async function getProductBySku(sku: string): Promise<Product> {
  try {
    const response = await fetch(`${API_BASE}/products/sku/${sku}`)
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Product not found')
      }
      throw new Error(`Failed to fetch product: ${response.status} ${response.statusText}`)
    }
    
    const product = await response.json()
    return product
  } catch (error) {
    console.error('Error fetching product:', error)
    throw error
  }
}

/**
 * Create a new product
 */
export async function createProduct(productData: ProductCreate): Promise<Product> {
  try {
    const response = await fetch(`${API_BASE}/products`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(productData),
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Failed to create product: ${response.status}`)
    }
    
    const product = await response.json()
    return product
  } catch (error) {
    console.error('Error creating product:', error)
    throw error
  }
}

/**
 * Update an existing product
 */
export async function updateProduct(
  productId: number, 
  productData: Partial<ProductCreate>
): Promise<Product> {
  try {
    const response = await fetch(`${API_BASE}/products/${productId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(productData),
    })
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Product not found')
      }
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Failed to update product: ${response.status}`)
    }
    
    const product = await response.json()
    return product
  } catch (error) {
    console.error('Error updating product:', error)
    throw error
  }
}
