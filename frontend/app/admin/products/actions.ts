"use server"

import { createProduct } from "@/lib/dal/products"
import { revalidatePath } from "next/cache"

export async function createProductAction(formData: FormData) {
  try {
    const name = formData.get("name") as string
    const description = formData.get("description") as string
    const price = parseFloat(formData.get("price") as string)
    const stock_qty = parseInt(formData.get("stock_qty") as string) || 0
    const image_url = formData.get("image_url") as string || undefined

    if (!name || !description || isNaN(price)) {
      throw new Error("Missing required fields")
    }

    await createProduct({
      name,
      description,
      price,
      stock_qty,
      image_url,
    })

    // Revalidate the products page to refresh the data
    revalidatePath("/admin/products")

    // Return success response
    return { success: true }
  } catch (error) {
    // Return error response
    return {
      success: false,
      error: error instanceof Error ? error.message : "Failed to create product"
    }
  }
}
