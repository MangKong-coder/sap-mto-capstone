"use client"

import Link from "next/link"
import { ShoppingCart, Package } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useCartStore } from "@/lib/cart-store"

export function Header() {
  const totalItems = useCartStore((state) => state.getTotalItems())

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
            <span className="font-bold text-lg text-primary-foreground">M</span>
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-lg leading-none">Mapúa Bookstore</span>
            <span className="text-xs text-muted-foreground">Official Merchandise</span>
          </div>
        </Link>

        <nav className="flex items-center gap-2">
          <Button variant="ghost" asChild>
            <Link href="/orders" className="flex items-center gap-2">
              <Package className="h-4 w-4" />
              <span className="hidden sm:inline">My Orders</span>
            </Link>
          </Button>
          <Button variant="ghost" asChild className="relative">
            <Link href="/cart" className="flex items-center gap-2">
              <ShoppingCart className="h-4 w-4" />
              <span className="hidden sm:inline">Cart</span>
              {totalItems > 0 && (
                <Badge
                  variant="destructive"
                  className="absolute -right-1 -top-1 h-5 w-5 rounded-full p-0 text-xs flex items-center justify-center"
                >
                  {totalItems}
                </Badge>
              )}
            </Link>
          </Button>
        </nav>
      </div>
    </header>
  )
}
