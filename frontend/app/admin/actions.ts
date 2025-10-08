/**
 * Server Actions for Products Management
 */

"use server"

import { revalidatePath } from "next/cache"
import { createBilling, getBillings, sendInvoice } from "@/lib/dal/billings"
import { updateDeliveryStatus, getDeliveries } from "@/lib/dal/deliveries"
import { updateProductionStatus, getProductionOrders } from "@/lib/dal/production-orders"
import { toast } from "sonner"

/**
 * Create a billing for a sales order
 */
export async function createBillingAction(formData: FormData) {
  const salesOrderId = Number(formData.get("salesOrderId"))
  if (!Number.isFinite(salesOrderId)) {
    throw new Error("salesOrderId is required to create billing")
  }
  try {
    await createBilling(salesOrderId)
    revalidatePath("/admin/billings")
  } catch (error) {
    console.error("Failed to create billing:", error)
    throw error
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

/**
 * Send invoice email for a sales order
 */
export async function sendInvoiceAction(formData: FormData) {
  const salesOrderId = Number(formData.get("salesOrderId"))
  if (!Number.isFinite(salesOrderId)) {
    throw new Error("salesOrderId is required to send invoice")
  }
  try {
    await sendInvoice(salesOrderId)
    revalidatePath("/admin/billings")
    toast.success("Invoice sent successfully")
  } catch (error) {
    console.error("Failed to send invoice:", error)
    toast.error("Failed to send invoice")
  }
}
