"use client"

import Image from "next/image"
import { ShoppingCart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useCartStore } from "@/lib/cart-store"
import type { Product } from "@/lib/types"
import { toast } from "sonner"

interface ProductCardProps {
  product: Product
}

export function ProductCard({ product }: ProductCardProps) {
  const addItem = useCartStore((state) => state.addItem)

  const handleAddToCart = () => {
    addItem(product, 1)
    toast("Added to cart", {
      description: `${product.name} has been added to your cart.`,
    })
  }

  return (
    <Card className="group overflow-hidden transition-shadow hover:shadow-lg">
      <CardHeader className="p-0">
        <div className="relative aspect-square overflow-hidden bg-muted">
          <img
            src={product.image_url || "/placeholder.svg"}
            alt={product.name}
            className="object-cover transition-transform group-hover:scale-105"
          />
          {product.stock_qty > 0 && product.stock_qty < 20 && (
            <Badge variant="secondary" className="absolute right-2 top-2">
              Low Stock
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="p-4">
        <h3 className="font-semibold text-lg leading-tight text-balance">{product.name}</h3>
        <p className="mt-2 text-muted-foreground text-sm line-clamp-2 text-pretty">{product.description}</p>
        <div className="mt-3 flex items-center justify-between">
          <span className="font-bold text-2xl text-primary">₱{product.price.toFixed(2)}</span>
          <span className="text-muted-foreground text-sm">{product.stock_qty} in stock</span>
        </div>
      </CardContent>
      <CardFooter className="p-4 pt-0">
        <Button onClick={handleAddToCart} className="w-full" disabled={product.stock_qty === 0}>
          <ShoppingCart className="mr-2 h-4 w-4" />
          {product.stock_qty === 0 ? "Out of Stock" : "Add to Cart"}
        </Button>
      </CardFooter>
    </Card>
  )
}
