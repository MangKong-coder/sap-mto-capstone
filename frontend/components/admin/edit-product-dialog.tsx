"use client"

import { useState, useTransition, useEffect } from "react"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { toast } from "sonner"
import { Edit, Loader2 } from "lucide-react"
import { Product } from "@/lib/types"
import { updateProductAction } from "@/app/admin/products/actions"

interface EditProductDialogProps {
  product: Product
  children?: React.ReactNode
}

export function EditProductDialog({ product, children }: EditProductDialogProps) {
  const [open, setOpen] = useState(false)
  const [isPending, startTransition] = useTransition()

  const handleSubmit = async (formData: FormData) => {
    startTransition(async () => {
      try {
        const result = await updateProductAction(product.id, formData)
        if (result.success) {
          toast.success("Product updated successfully!")
          setOpen(false)
        } else {
          toast.error(result.error)
        }
      } catch (error) {
        toast.error("Failed to update product")
      }
    })
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {children || (
          <Button
            size="sm"
            variant="outline"
            className="border-zinc-300 text-zinc-700 hover:bg-zinc-100 bg-transparent"
          >
            <Edit className="h-3 w-3" />
          </Button>
        )}
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit Product</DialogTitle>
          <DialogDescription>
            Update the product details below.
          </DialogDescription>
        </DialogHeader>
        <form action={handleSubmit} className="space-y-4">
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="name">Product Name</Label>
              <Input
                id="name"
                name="name"
                defaultValue={product.name}
                placeholder="Enter product name"
                required
                disabled={isPending}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                name="description"
                defaultValue={product.description}
                placeholder="Enter product description"
                required
                disabled={isPending}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="price">Price (₱)</Label>
              <Input
                id="price"
                name="price"
                type="number"
                step="0.01"
                min="0"
                defaultValue={product.price}
                placeholder="0.00"
                required
                disabled={isPending}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="image_url">Image URL (Optional)</Label>
              <Input
                id="image_url"
                name="image_url"
                type="url"
                defaultValue={product.image_url || ""}
                placeholder="https://example.com/image.jpg"
                disabled={isPending}
              />
            </div>
          </div>
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
              disabled={isPending}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isPending}
              className="bg-zinc-900 hover:bg-zinc-800 text-white"
            >
              {isPending ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Updating...
                </>
              ) : (
                "Update Product"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
