import { ShoppingCart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { useCartStore } from "@/lib/cart-store"
import { createOrderAction } from "@/app/orders/actions"

export function CartSummary() {
  const items = useCartStore((state) => state.items)
  const totalAmount = useCartStore((state) => state.getTotalAmount())

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
        <form action={createOrderAction} className="w-full">
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
            disabled={items.length === 0}
          >
            <ShoppingCart className="mr-2 h-4 w-4" />
            Place Order
          </Button>
        </form>
      </CardFooter>
    </Card>
  )
}
