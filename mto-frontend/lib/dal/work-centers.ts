/**
 * Data Access Layer for Work Centers
 * 
 * This module provides functions to interact with the backend API
 * for work center-related operations.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export interface WorkCenter {
  id: number
  name: string
  description?: string
  address?: string
  created_at: string
  updated_at: string
}

export interface WorkCenterCreate {
  name: string
  description?: string
  address?: string
}

/**
 * Fetch work centers from the backend
 */
export async function getWorkCenters(page: number = 1, size: number = 100): Promise<WorkCenter[]> {
  try {
    const response = await fetch(`${API_BASE}/work-centers?page=${page}&size=${size}`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch work centers: ${response.status} ${response.statusText}`)
    }
    
    const workCenters = await response.json()
    return workCenters
  } catch (error) {
    console.error('Error fetching work centers:', error)
    throw new Error('Failed to fetch work centers')
  }
}

/**
 * Fetch a single work center by ID
 */
export async function getWorkCenterById(workCenterId: number): Promise<WorkCenter> {
  try {
    const response = await fetch(`${API_BASE}/work-centers/${workCenterId}`)
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Work center not found')
      }
      throw new Error(`Failed to fetch work center: ${response.status} ${response.statusText}`)
    }
    
    const workCenter = await response.json()
    return workCenter
  } catch (error) {
    console.error('Error fetching work center:', error)
    throw error
  }
}

/**
 * Create a new work center
 */
export async function createWorkCenter(workCenterData: WorkCenterCreate): Promise<WorkCenter> {
  try {
    const response = await fetch(`${API_BASE}/work-centers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workCenterData),
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Failed to create work center: ${response.status}`)
    }
    
    const workCenter = await response.json()
    return workCenter
  } catch (error) {
    console.error('Error creating work center:', error)
    throw error
  }
}

/**
 * Update an existing work center
 */
export async function updateWorkCenter(workCenterId: number, workCenterData: WorkCenterCreate): Promise<WorkCenter> {
  try {
    const response = await fetch(`${API_BASE}/work-centers/${workCenterId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workCenterData),
    })
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Work center not found')
      }
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Failed to update work center: ${response.status}`)
    }
    
    const workCenter = await response.json()
    return workCenter
  } catch (error) {
    console.error('Error updating work center:', error)
    throw error
  }
}

/**
 * Delete a work center
 */
export async function deleteWorkCenter(workCenterId: number): Promise<void> {
  try {
    const response = await fetch(`${API_BASE}/work-centers/${workCenterId}`, {
      method: 'DELETE',
    })
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Work center not found')
      }
      throw new Error(`Failed to delete work center: ${response.status}`)
    }
  } catch (error) {
    console.error('Error deleting work center:', error)
    throw error
  }
}
