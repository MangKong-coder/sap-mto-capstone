"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { mockProductionOrders } from "@/lib/mock-data"

interface CreateConfirmationDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function CreateConfirmationDialog({ open, onOpenChange }: CreateConfirmationDialogProps) {
  const [formData, setFormData] = useState({
    productionOrder: "",
    confirmedQuantity: "",
    confirmationDate: new Date().toISOString().split("T")[0],
    workCenter: "",
    notes: "",
  })

  const activeOrders = mockProductionOrders.filter(
    (order) => order.status === "Released" || order.status === "In Progress",
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("[v0] Creating production confirmation:", formData)
    // In a real app, this would call an API
    onOpenChange(false)
    setFormData({
      productionOrder: "",
      confirmedQuantity: "",
      confirmationDate: new Date().toISOString().split("T")[0],
      workCenter: "",
      notes: "",
    })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Create Production Confirmation</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="productionOrder">Production Order *</Label>
            <Select
              value={formData.productionOrder}
              onValueChange={(value) => setFormData({ ...formData, productionOrder: value })}
            >
              <SelectTrigger id="productionOrder">
                <SelectValue placeholder="Select production order" />
              </SelectTrigger>
              <SelectContent>
                {activeOrders.map((order) => (
                  <SelectItem key={order.id} value={order.productionOrderNumber}>
                    {order.productionOrderNumber} - {order.material}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="confirmedQuantity">Confirmed Quantity *</Label>
              <Input
                id="confirmedQuantity"
                type="number"
                placeholder="Enter quantity"
                value={formData.confirmedQuantity}
                onChange={(e) => setFormData({ ...formData, confirmedQuantity: e.target.value })}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirmationDate">Confirmation Date *</Label>
              <Input
                id="confirmationDate"
                type="date"
                value={formData.confirmationDate}
                onChange={(e) => setFormData({ ...formData, confirmationDate: e.target.value })}
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="workCenter">Work Center *</Label>
            <Select
              value={formData.workCenter}
              onValueChange={(value) => setFormData({ ...formData, workCenter: value })}
            >
              <SelectTrigger id="workCenter">
                <SelectValue placeholder="Select work center" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="wc-001">WC-001 - Assembly Line 1</SelectItem>
                <SelectItem value="wc-002">WC-002 - Assembly Line 2</SelectItem>
                <SelectItem value="wc-003">WC-003 - Quality Control</SelectItem>
                <SelectItem value="wc-004">WC-004 - Packaging</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Notes</Label>
            <Textarea
              id="notes"
              placeholder="Add any notes or comments..."
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              rows={4}
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit">Create Confirmation</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
