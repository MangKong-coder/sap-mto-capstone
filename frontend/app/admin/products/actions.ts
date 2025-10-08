"use server"

import { createProduct, updateProduct, deleteProduct } from "@/lib/dal/products"
import { revalidatePath } from "next/cache"

export async function createProductAction(formData: FormData) {
  try {
    const name = formData.get("name") as string
    const description = formData.get("description") as string
    const price = parseFloat(formData.get("price") as string)
    const image_url = formData.get("image_url") as string || undefined

    if (!name || !description || isNaN(price)) {
      throw new Error("Missing required fields")
    }

    await createProduct({
      name,
      description,
      price,
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

export async function updateProductAction(productId: number, formData: FormData) {
  try {
    const name = formData.get("name") as string
    const description = formData.get("description") as string
    const price = parseFloat(formData.get("price") as string)
    const image_url = formData.get("image_url") as string || undefined

    if (!name || !description || isNaN(price)) {
      throw new Error("Missing required fields")
    }

    await updateProduct(productId, {
      name,
      description,
      price,
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
      error: error instanceof Error ? error.message : "Failed to update product"
    }
  }
}

export async function deleteProductAction(productId: number) {
  try {
    await deleteProduct(productId)

    // Revalidate the products page to refresh the data
    revalidatePath("/admin/products")

    // Return success response
    return { success: true }
  } catch (error) {
    // Return error response
    return {
      success: false,
      error: error instanceof Error ? error.message : "Failed to delete product"
    }
  }
}
