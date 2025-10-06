"use client"

import { useState } from "react"
import { useAdminStore } from "@/lib/admin-store"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Search, Edit, Trash2 } from "lucide-react"
import Image from "next/image"

export default function ProductsPage() {
  const { products, updateProduct, deleteProduct } = useAdminStore()
  const [searchTerm, setSearchTerm] = useState("")

  const filteredProducts = products.filter(
    (product) =>
      product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.description.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">Product Management</h2>
          <p className="text-sm text-zinc-400">Manage product catalog and inventory</p>
        </div>
      </div>

      <Card className="border-zinc-800 bg-zinc-900">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-white">All Products</CardTitle>
            <div className="relative w-64">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" />
              <Input
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="border-zinc-700 bg-zinc-800 pl-9 text-white placeholder:text-zinc-500"
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-800">
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Product</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Description</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-400">Price</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-400">Stock</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Status</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-400">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredProducts.map((product) => (
                  <tr key={product.id} className="border-b border-zinc-800/50">
                    <td className="py-4">
                      <div className="flex items-center gap-3">
                        {product.image_url && (
                          <div className="relative h-10 w-10 overflow-hidden rounded-md bg-zinc-800">
                            <Image
                              src={product.image_url || "/placeholder.svg"}
                              alt={product.name}
                              fill
                              className="object-cover"
                            />
                          </div>
                        )}
                        <span className="text-sm font-medium text-white">{product.name}</span>
                      </div>
                    </td>
                    <td className="py-4 text-sm text-zinc-400">{product.description}</td>
                    <td className="py-4 text-right text-sm font-medium text-white">₱{product.price.toFixed(2)}</td>
                    <td className="py-4 text-right text-sm text-zinc-300">{product.stock_qty}</td>
                    <td className="py-4">
                      <Badge
                        variant="secondary"
                        className={
                          product.stock_qty > 10
                            ? "bg-green-500/10 text-green-500"
                            : product.stock_qty > 0
                              ? "bg-yellow-500/10 text-yellow-500"
                              : "bg-red-500/10 text-red-500"
                        }
                      >
                        {product.stock_qty > 10 ? "In Stock" : product.stock_qty > 0 ? "Low Stock" : "Out of Stock"}
                      </Badge>
                    </td>
                    <td className="py-4 text-right">
                      <div className="flex justify-end gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          className="border-zinc-700 text-zinc-300 hover:bg-zinc-800 bg-transparent"
                        >
                          <Edit className="h-3 w-3" />
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => deleteProduct(product.id)}
                          className="border-zinc-700 text-red-400 hover:bg-zinc-800"
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
