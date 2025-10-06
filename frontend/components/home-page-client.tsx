"use client"

import { ProductGrid } from "@/components/product-grid"
import { Product } from "@/lib/types"

interface HomePageProps {
  products: Product[]
}

export function HomePageClient({ products }: HomePageProps) {
  return (
    <main className="px-12 py-8">
      <div className="mb-8 space-y-2">
        <h1 className="font-bold text-4xl text-balance">Official Mapúa Merchandise</h1>
        <p className="text-muted-foreground text-lg text-pretty">
          Browse our collection of authentic Cardinals apparel and accessories
        </p>
      </div>

      <ProductGrid products={products} />
    </main>
  )
}
