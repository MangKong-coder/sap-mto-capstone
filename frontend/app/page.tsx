import { ProductGrid } from "@/components/product-grid"
import { mockProducts } from "@/lib/mock-data"

export default function HomePage() {
  return (
    <main className="px-12 py-8">
      <div className="mb-8 space-y-2">
        <h1 className="font-bold text-4xl text-balance">Official Mapúa Merchandise</h1>
        <p className="text-muted-foreground text-lg text-pretty">
          Browse our collection of authentic Cardinals apparel and accessories
        </p>
      </div>

      <ProductGrid products={mockProducts} />
    </main>
  )
}
