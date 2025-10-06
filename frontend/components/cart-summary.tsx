"use client"

import { useRouter } from "next/navigation"
import { ShoppingCart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { useCartStore } from "@/lib/cart-store"
import { useOrdersStore } from "@/lib/orders-store"
import { mockCustomer } from "@/lib/mock-data"
import { toast } from "sonner"

export function CartSummary() {
  const router = useRouter()
  const items = useCartStore((state) => state.items)
  const totalAmount = useCartStore((state) => state.getTotalAmount())
  const clearCart = useCartStore((state) => state.clearCart)
  const createOrder = useOrdersStore((state) => state.createOrder)

  const handlePlaceOrder = () => {
    const orderItems = items.map((item) => ({
      product_id: item.product.id,
      quantity: item.quantity,
      subtotal: item.product.price * item.quantity,
    }))

    const newOrder = createOrder(mockCustomer.id, orderItems, totalAmount)

    clearCart()

    toast("Order placed successfully!", {
      description: `Order #${newOrder.id} has been created.`,
    })

    router.push(`/orders/${newOrder.id}/confirmation`)
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
        <Button onClick={handlePlaceOrder} className="w-full" size="lg">
          <ShoppingCart className="mr-2 h-4 w-4" />
          Place Order
        </Button>
      </CardFooter>
    </Card>
  )
}
