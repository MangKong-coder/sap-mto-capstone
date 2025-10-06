/**
 * Server Actions for Products Management
 */

"use server"

import { revalidatePath } from "next/navigation"
import { createBilling, getBillings } from "@/lib/dal/billings"
import { updateDeliveryStatus, getDeliveries } from "@/lib/dal/deliveries"
import { updateProductionStatus, getProductionOrders } from "@/lib/dal/production-orders"

/**
 * Create a billing for a sales order
 */
export async function createBillingAction(salesOrderId: number) {
  try {
    await createBilling(salesOrderId)
    revalidatePath("/admin/billings")
    return { success: true, message: "Billing created successfully" }
  } catch (error) {
    console.error("Failed to create billing:", error)
    return {
      success: false,
      message: error instanceof Error ? error.message : "Failed to create billing"
    }
  }
}

/**
 * Update delivery status
 */
export async function updateDeliveryStatusAction(deliveryId: number, status: string) {
  try {
    await updateDeliveryStatus(deliveryId, status)
    revalidatePath("/admin/deliveries")
    return { success: true, message: "Delivery status updated successfully" }
  } catch (error) {
    console.error("Failed to update delivery status:", error)
    return {
      success: false,
      message: error instanceof Error ? error.message : "Failed to update delivery status"
    }
  }
}

/**
 * Update production order status
 */
export async function updateProductionStatusAction(productionId: number, status: string) {
  try {
    await updateProductionStatus(productionId, status)
    revalidatePath("/admin/production")
    return { success: true, message: "Production status updated successfully" }
  } catch (error) {
    console.error("Failed to update production status:", error)
    return {
      success: false,
      message: error instanceof Error ? error.message : "Failed to update production status"
    }
  }
}
