/**
 * Data Access Layer for Orders
 * 
 * This module provides functions to interact with the backend API
 * for order-related operations. It transforms backend responses
 * to match frontend data structures.
 */

import { SalesOrder } from '../types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

/**
 * Transform backend enriched order response to frontend SalesOrder type
 */
function transformBackendOrder(backendOrder: any): SalesOrder {
  return {
    id: backendOrder.id.toString(),
    orderNumber: backendOrder.id.toString(), // Using ID as order number
    customer: backendOrder.customer_name,
    customerType: backendOrder.customer_type === 'DEPARTMENT' ? 'Department' : 'Campus',
    material: backendOrder.items?.[0]?.product_name || 'Multiple Items',
    quantity: backendOrder.total_quantity,
    deliveryDate: backendOrder.delivery_date || new Date().toISOString(),
    status: mapBackendStatus(backendOrder.status),
    createdDate: backendOrder.created_at,
    netValue: backendOrder.net_value,
    plant: backendOrder.work_center_name,
    priority: mapBackendPriority(backendOrder.priority),
  }
}

/**
 * Map backend status to frontend status
 */
function mapBackendStatus(backendStatus: string): SalesOrder['status'] {
  const statusMap: Record<string, SalesOrder['status']> = {
    'NEW': 'Open',
    'CONFIRMED': 'In Planning',
    'IN_PROGRESS': 'In Production',
    'COMPLETED': 'Delivered',
    'BILLED': 'Billed',
    'CANCELLED': 'Open'
  }
  return statusMap[backendStatus] || 'Open'
}

/**
 * Map backend priority to frontend priority
 */
function mapBackendPriority(backendPriority: string): SalesOrder['priority'] {
  const priorityMap: Record<string, SalesOrder['priority']> = {
    'STANDARD': 'Standard',
    'URGENT': 'Urgent',
    'RUSH': 'Rush'
  }
  return priorityMap[backendPriority] || 'Standard'
}

/**
 * Fetch orders from the backend with enriched data
 */
export async function getOrders(page: number = 1, size: number = 20): Promise<SalesOrder[]> {
  try {
    const response = await fetch(`${API_BASE}/orders/enriched?page=${page}&size=${size}`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch orders: ${response.status} ${response.statusText}`)
    }
    
    const backendOrders = await response.json()
    return backendOrders.map(transformBackendOrder)
  } catch (error) {
    console.error('Error fetching orders:', error)
    throw new Error('Failed to fetch orders')
  }
}

/**
 * Fetch a single order by ID with enriched data
 */
export async function getOrderById(orderId: string): Promise<SalesOrder> {
  try {
    const response = await fetch(`${API_BASE}/orders/${orderId}/enriched`)
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Order not found')
      }
      throw new Error(`Failed to fetch order: ${response.status} ${response.statusText}`)
    }
    
    const backendOrder = await response.json()
    return transformBackendOrder(backendOrder)
  } catch (error) {
    console.error('Error fetching order:', error)
    throw error
  }
}

/**
 * Create a new order
 */
export async function createOrder(orderData: {
  customer_id: number
  delivery_date?: string
  priority?: string
  work_center_id: number
  items: Array<{
    product_id: number
    quantity: number
    unit_price: number
  }>
}): Promise<SalesOrder> {
  try {
    const response = await fetch(`${API_BASE}/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(orderData),
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Failed to create order: ${response.status}`)
    }
    
    const backendOrder = await response.json()
    return transformBackendOrder(backendOrder)
  } catch (error) {
    console.error('Error creating order:', error)
    throw error
  }
}

/**
 * Cancel an order
 */
export async function cancelOrder(orderId: string): Promise<SalesOrder> {
  try {
    const response = await fetch(`${API_BASE}/orders/${orderId}/cancel`, {
      method: 'PUT',
    })
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Order not found')
      }
      if (response.status === 409) {
        throw new Error('Order cannot be cancelled')
      }
      throw new Error(`Failed to cancel order: ${response.status}`)
    }
    
    const backendOrder = await response.json()
    return transformBackendOrder(backendOrder)
  } catch (error) {
    console.error('Error cancelling order:', error)
    throw error
  }
}

/**
 * Get orders by customer ID
 */
export async function getOrdersByCustomer(customerId: number): Promise<SalesOrder[]> {
  try {
    const response = await fetch(`${API_BASE}/orders/customer/${customerId}`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch customer orders: ${response.status}`)
    }
    
    const backendOrders = await response.json()
    return backendOrders.map(transformBackendOrder)
  } catch (error) {
    console.error('Error fetching customer orders:', error)
    throw new Error('Failed to fetch customer orders')
  }
}
