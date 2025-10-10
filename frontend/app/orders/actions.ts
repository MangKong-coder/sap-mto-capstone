"use server"

import { createOrder } from "@/lib/dal/orders"
import { revalidateOrders } from "@/lib/cache-utils"
import type { OrderDetail } from "@/lib/dal/orders"

export async function createOrderAction(formData: FormData): Promise<OrderDetail> {
  try {
    const customerId = parseInt(formData.get("customerId") as string)
    const itemsData = formData.get("items") as string

    if (!customerId || !itemsData) {
      throw new Error("Missing required fields")
    }

    const items = JSON.parse(itemsData)
    const newOrder = await createOrder(customerId, items)

    // Revalidate all order-related caches
    revalidateOrders(newOrder.id)

    // Return the order data for client-side handling
    return newOrder
  } catch (error) {
    console.error("Failed to create order:", error)
    throw error instanceof Error ? error : new Error("Failed to create order")
  }
}
