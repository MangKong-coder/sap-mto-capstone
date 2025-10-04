"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface CreateDeliveryDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function CreateDeliveryDialog({ open, onOpenChange }: CreateDeliveryDialogProps) {
  const [formData, setFormData] = useState({
    salesOrder: "",
    deliveryDate: new Date().toISOString().split("T")[0],
    quantity: "",
    shippingPoint: "",
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("[v0] Creating delivery:", formData)
    onOpenChange(false)
    setFormData({
      salesOrder: "",
      deliveryDate: new Date().toISOString().split("T")[0],
      quantity: "",
      shippingPoint: "",
    })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Create Outbound Delivery (VL01N)</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="salesOrder">Sales Order *</Label>
            <Select
              value={formData.salesOrder}
              onValueChange={(value) => setFormData({ ...formData, salesOrder: value })}
            >
              <SelectTrigger id="salesOrder">
                <SelectValue placeholder="Select sales order" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="SO-2024-001">SO-2024-001 - Acme Corporation</SelectItem>
                <SelectItem value="SO-2024-002">SO-2024-002 - Global Industries</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="quantity">Quantity *</Label>
              <Input
                id="quantity"
                type="number"
                placeholder="Enter quantity"
                value={formData.quantity}
                onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="deliveryDate">Delivery Date *</Label>
              <Input
                id="deliveryDate"
                type="date"
                value={formData.deliveryDate}
                onChange={(e) => setFormData({ ...formData, deliveryDate: e.target.value })}
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="shippingPoint">Shipping Point *</Label>
            <Select
              value={formData.shippingPoint}
              onValueChange={(value) => setFormData({ ...formData, shippingPoint: value })}
            >
              <SelectTrigger id="shippingPoint">
                <SelectValue placeholder="Select shipping point" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="sp-001">SP-001 - Main Warehouse</SelectItem>
                <SelectItem value="sp-002">SP-002 - Distribution Center</SelectItem>
                <SelectItem value="sp-003">SP-003 - Regional Hub</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit">Create Delivery</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
