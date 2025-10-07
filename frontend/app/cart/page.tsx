"use client"

import Link from "next/link"
import { ShoppingBag, ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { CartItemList } from "@/components/cart-item-list"
import { CartSummary } from "@/components/cart-summary"
import { useCartStore } from "@/lib/cart-store"

export default function CartPage() {
  const items = useCartStore((state) => state.items)

  if (items.length === 0) {
    return (
      <main className="px-12 py-16">
        <div className="mx-auto flex max-w-md flex-col items-center gap-4 text-center">
          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-muted">
            <ShoppingBag className="h-10 w-10 text-muted-foreground" />
          </div>
          <h1 className="font-bold text-2xl">Your cart is empty</h1>
          <p className="text-muted-foreground text-pretty">
            Start shopping to add items to your cart and place your order.
          </p>
          <Button asChild className="mt-4">
            <Link href="/">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Continue Shopping
            </Link>
          </Button>
        </div>
      </main>
    )
  }

  return (
    <main className="px-12 py-8">
      <div className="mb-6">
        <h1 className="font-bold text-3xl">Shopping Cart</h1>
        <p className="text-muted-foreground">Review your items before placing your order</p>
      </div>

      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <CartItemList />
        </div>
        <div className="lg:col-span-1">
          <CartSummary />
        </div>
      </div>
    </main>
  )
}
