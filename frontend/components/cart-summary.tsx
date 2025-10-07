"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { ShoppingCart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { useCartStore } from "@/lib/cart-store"
import { createOrderAction } from "@/app/orders/actions"

export function CartSummary() {
  const router = useRouter()
  const items = useCartStore((state) => state.items)
  const totalAmount = useCartStore((state) => state.getTotalAmount())
  const clearCart = useCartStore((state) => state.clearCart)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (formData: FormData) => {
    setIsSubmitting(true)

    try {
      const order = await createOrderAction(formData)

      // Clear the cart after successful order creation
      clearCart()

      // Redirect to order confirmation page
      router.push(`/orders/${order.id}/confirmation`)
    } catch (error) {
      console.error("Failed to create order:", error)
      // Here you could add toast notifications or error handling
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Card className="sticky top-20">
      <CardHeader>
        <CardTitle>Order Summary</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Subtotal</span>
            <span>₱{totalAmount.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Shipping</span>
            <span>Free</span>
          </div>
        </div>
        <Separator />
        <div className="flex justify-between font-semibold text-lg">
          <span>Total</span>
          <span className="text-primary">₱{totalAmount.toFixed(2)}</span>
        </div>
      </CardContent>
      <CardFooter>
        <form action={handleSubmit} className="w-full">
          <input type="hidden" name="customerId" value="1" />
          <input
            type="hidden"
            name="items"
            value={JSON.stringify(
              items.map((item) => ({
                product_id: item.product.id,
                quantity: item.quantity
              }))
            )}
          />
          <Button
            type="submit"
            className="w-full"
            size="lg"
            disabled={items.length === 0 || isSubmitting}
          >
            <ShoppingCart className="mr-2 h-4 w-4" />
            {isSubmitting ? "Processing..." : "Place Order"}
          </Button>
        </form>
      </CardFooter>
    </Card>
  )
}
