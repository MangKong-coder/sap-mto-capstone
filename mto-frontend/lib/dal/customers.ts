/**
 * Data Access Layer for Customers
 * 
 * This module provides functions to interact with the backend API
 * for customer-related operations.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export interface Customer {
  id: number
  name: string
  email?: string
  phone?: string
  address?: string
  customer_type: 'DEPARTMENT' | 'CAMPUS' | 'STUDENT' | 'VENDOR'
  created_at: string
  updated_at: string
}

export interface CustomerCreate {
  name: string
  email?: string
  phone?: string
  address?: string
  customer_type: 'DEPARTMENT' | 'CAMPUS' | 'STUDENT' | 'VENDOR'
}

/**
 * Fetch customers from the backend
 */
export async function getCustomers(page: number = 1, size: number = 20): Promise<Customer[]> {
  try {
    const response = await fetch(`${API_BASE}/customers?page=${page}&size=${size}`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch customers: ${response.status} ${response.statusText}`)
    }
    
    const customers = await response.json()
    return customers
  } catch (error) {
    console.error('Error fetching customers:', error)
    throw new Error('Failed to fetch customers')
  }
}

/**
 * Fetch a single customer by ID
 */
export async function getCustomerById(customerId: number): Promise<Customer> {
  try {
    const response = await fetch(`${API_BASE}/customers/${customerId}`)
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Customer not found')
      }
      throw new Error(`Failed to fetch customer: ${response.status} ${response.statusText}`)
    }
    
    const customer = await response.json()
    return customer
  } catch (error) {
    console.error('Error fetching customer:', error)
    throw error
  }
}

/**
 * Create a new customer
 */
export async function createCustomer(customerData: CustomerCreate): Promise<Customer> {
  try {
    const response = await fetch(`${API_BASE}/customers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(customerData),
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Failed to create customer: ${response.status}`)
    }
    
    const customer = await response.json()
    return customer
  } catch (error) {
    console.error('Error creating customer:', error)
    throw error
  }
}

/**
 * Update an existing customer
 */
export async function updateCustomer(
  customerId: number, 
  customerData: Partial<CustomerCreate>
): Promise<Customer> {
  try {
    const response = await fetch(`${API_BASE}/customers/${customerId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(customerData),
    })
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Customer not found')
      }
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Failed to update customer: ${response.status}`)
    }
    
    const customer = await response.json()
    return customer
  } catch (error) {
    console.error('Error updating customer:', error)
    throw error
  }
}
