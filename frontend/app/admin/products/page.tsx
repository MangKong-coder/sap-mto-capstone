import { Suspense } from "react"
import { getProducts } from "@/lib/dal"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Edit, Trash2, Package } from "lucide-react"
import Image from "next/image"
import { CreateProductDialog } from "@/components/admin/create-product-dialog"
import { Product } from "@/lib/types"

export default function ProductsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-zinc-900">Product Management</h2>
          <p className="text-sm text-zinc-600">Manage product catalog and inventory</p>
        </div>
        <CreateProductDialog />
      </div>

      <Suspense fallback={<ProductsTableSkeleton />}>
        <ProductsTable />
      </Suspense>
    </div>
  )
}

async function ProductsTable() {
  try {
    const products = await getProducts()

    return (
      <Card className="border-zinc-200 bg-white">
        <CardHeader>
          <CardTitle className="text-zinc-900">All Products</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-200">
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Product</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Description</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-600">Price</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-600">Stock</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Status</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-600">Actions</th>
                </tr>
              </thead>
              <tbody>
                {products.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-6 text-center text-sm text-zinc-500">
                      No products available.
                    </td>
                  </tr>
                ) : (
                  products.map((product: Product) => (
                    <tr key={product.id} className="border-b border-zinc-100">
                      <td className="py-4">
                        <div className="flex items-center gap-3">
                          {product.image_url && (
                            <div className="relative h-10 w-10 overflow-hidden rounded-md bg-zinc-100">
                              <img
                                src={product.image_url || "/placeholder.svg"}
                                alt={product.name}
                                className="object-cover"
                              />
                            </div>
                          )}
                          <span className="text-sm font-medium text-zinc-900">{product.name}</span>
                        </div>
                      </td>
                      <td className="py-4 text-sm text-zinc-600">{product.description}</td>
                      <td className="py-4 text-right text-sm font-medium text-zinc-900">₱{product.price.toFixed(2)}</td>
                      <td className="py-4 text-right text-sm text-zinc-700">{product.stock_qty || 0}</td>
                      <td className="py-4">
                        <Badge
                          variant="secondary"
                          className={
                            (product.stock_qty || 0) > 10
                              ? "bg-green-500/10 text-green-500"
                              : (product.stock_qty || 0) > 0
                                ? "bg-yellow-500/10 text-yellow-500"
                                : "bg-red-500/10 text-red-500"
                          }
                        >
                          {(product.stock_qty || 0) > 10 ? "In Stock" : (product.stock_qty || 0) > 0 ? "Low Stock" : "Out of Stock"}
                        </Badge>
                      </td>
                      <td className="py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            size="sm"
                            variant="outline"
                            className="border-zinc-300 text-zinc-700 hover:bg-zinc-100 bg-transparent"
                          >
                            <Edit className="h-3 w-3" />
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            className="border-zinc-300 text-red-500 hover:bg-zinc-100"
                          >
                            <Trash2 className="h-3 w-3" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    )
  } catch (error) {
    const message = error instanceof Error ? error.message : "Failed to load products"

    return (
      <Card className="border-red-200 bg-red-50">
        <CardContent className="pt-6">
          <p className="text-sm text-red-600">{message}</p>
        </CardContent>
      </Card>
    )
  }
}

function ProductsTableSkeleton() {
  return (
    <Card className="border-zinc-200 bg-white">
      <CardHeader>
        <CardTitle className="text-zinc-900">All Products</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {[...Array(3)].map((_, index) => (
            <div key={index} className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-md bg-zinc-200 animate-pulse" />
                <div className="h-4 w-32 rounded bg-zinc-200 animate-pulse" />
              </div>
              <div className="h-4 w-24 rounded bg-zinc-200 animate-pulse" />
              <div className="h-4 w-16 rounded bg-zinc-200 animate-pulse" />
              <div className="h-4 w-20 rounded bg-zinc-200 animate-pulse" />
              <div className="flex gap-2">
                <div className="h-8 w-8 rounded bg-zinc-200 animate-pulse" />
                <div className="h-8 w-8 rounded bg-zinc-200 animate-pulse" />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
