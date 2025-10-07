"use server"

import { createOrder } from "@/lib/dal/orders"
import { revalidatePath } from "next/cache"

export async function createOrderAction(formData: FormData): Promise<void> {
  try {
    const customerId = parseInt(formData.get("customerId") as string)
    const itemsData = formData.get("items") as string

    if (!customerId || !itemsData) {
      throw new Error("Missing required fields")
    }

    const items = JSON.parse(itemsData)

    const newOrder = await createOrder(customerId, items)

    // Revalidate paths that might show orders
    revalidatePath("/orders")
    revalidatePath("/admin/orders")
  } catch (error) {
    console.error("Failed to create order:", error)
    throw error instanceof Error ? error : new Error("Failed to create order")
  }
}
