/**
 * Server Actions for Admin Order Management
 * These actions run on the server and handle order mutations.
 */

"use server"

import { revalidatePath } from "next/cache"

import {
  completeProductionOrder,
  deleteOrder,
  getOrderDetail,
  markProductionInProgress,
  startProduction,
  updateOrderStatus,
} from "@/lib/dal/orders"
import { SalesOrderStatus } from "@/lib/types"

/**
 * Start production for a sales order
 */
export async function startProductionAction(orderId: number) {
  try {
    await startProduction(orderId)
    revalidatePath("/admin/orders")
    return { success: true, message: "Production started successfully" }
  } catch (error) {
    console.error("Failed to start production:", error)
    return {
      success: false,
      message: error instanceof Error ? error.message : "Failed to start production"
    }
  }
}

/**
 * Mark an order as ready for delivery (complete production process)
 */
export async function markOrderReadyAction(orderId: number) {
  try {
    // Get the order details to find the latest production order
    const orderDetail = await getOrderDetail(orderId)

    if (!orderDetail.production_orders || orderDetail.production_orders.length === 0) {
      throw new Error("No production orders found for this order")
    }

    // Find the most recent production order
    const latestProductionOrder = orderDetail.production_orders
      .sort((a, b) => b.id - a.id)[0]

    // Mark production as in progress, then complete it
    await markProductionInProgress(latestProductionOrder.id)
    await completeProductionOrder(latestProductionOrder.id)

    revalidatePath("/admin/orders")
    return { success: true, message: "Order marked as ready for delivery" }
  } catch (error) {
    console.error("Failed to mark order ready:", error)
    return {
      success: false,
      message: error instanceof Error ? error.message : "Failed to mark order ready"
    }
  }
}

/**
 * Update the status of a sales order
 */
export async function updateOrderStatusAction(orderId: number, status: SalesOrderStatus) {
  try {
    await updateOrderStatus(orderId, status)
    revalidatePath("/admin/orders")
    return { success: true, message: "Order status updated successfully" }
  } catch (error) {
    console.error("Failed to update order status:", error)
    return {
      success: false,
      message: error instanceof Error ? error.message : "Failed to update order status"
    }
  }
}

/**
 * Delete a sales order
 */
export async function deleteOrderAction(orderId: number) {
  try {
    await deleteOrder(orderId)
    revalidatePath("/admin/orders")
    return { success: true, message: "Order deleted successfully" }
  } catch (error) {
    console.error("Failed to delete order:", error)
    return {
      success: false,
      message: error instanceof Error ? error.message : "Failed to delete order"
    }
  }
}
