"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { PlannedOrder } from "@/lib/types"
import { ArrowRight, CheckCircle } from "lucide-react"

interface ConvertToProductionDialogProps {
  order: PlannedOrder
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function ConvertToProductionDialog({ order, open, onOpenChange }: ConvertToProductionDialogProps) {
  const [formData, setFormData] = useState({
    startDate: order.startDate,
    endDate: order.endDate,
    quantity: order.quantity.toString(),
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("[v0] Converting to production order:", { plannedOrder: order, ...formData })
    // In a real app, this would call an API
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Convert to Production Order (CO01)</DialogTitle>
        </DialogHeader>

        <div className="bg-muted/50 border border-border rounded-lg p-4 mb-4">
          <div className="flex items-center gap-3 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-yellow-500/20 flex items-center justify-center">
                <CheckCircle className="w-4 h-4 text-yellow-500" />
              </div>
              <div>
                <div className="font-medium text-foreground">Planned Order</div>
                <div className="text-muted-foreground">{order.plannedOrderNumber}</div>
              </div>
            </div>
            <ArrowRight className="w-5 h-5 text-muted-foreground" />
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center">
                <CheckCircle className="w-4 h-4 text-purple-500" />
              </div>
              <div>
                <div className="font-medium text-foreground">Production Order</div>
                <div className="text-muted-foreground">PRO-{order.plannedOrderNumber.split("-")[2]}</div>
              </div>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Sales Order</Label>
              <Input value={order.salesOrderNumber} disabled />
            </div>

            <div className="space-y-2">
              <Label>Plant</Label>
              <Input value={order.plant} disabled />
            </div>
          </div>

          <div className="space-y-2">
            <Label>Material</Label>
            <Input value={order.material} disabled />
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="quantity">Quantity *</Label>
              <Input
                id="quantity"
                type="number"
                value={formData.quantity}
                onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="startDate">Start Date *</Label>
              <Input
                id="startDate"
                type="date"
                value={formData.startDate}
                onChange={(e) => setFormData({ ...formData, startDate: e.target.value })}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="endDate">End Date *</Label>
              <Input
                id="endDate"
                type="date"
                value={formData.endDate}
                onChange={(e) => setFormData({ ...formData, endDate: e.target.value })}
                required
              />
            </div>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit">Convert to Production Order</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
