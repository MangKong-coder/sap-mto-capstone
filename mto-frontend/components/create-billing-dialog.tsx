"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface CreateBillingDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function CreateBillingDialog({ open, onOpenChange }: CreateBillingDialogProps) {
  const [formData, setFormData] = useState({
    delivery: "",
    billingDate: new Date().toISOString().split("T")[0],
    paymentTerms: "",
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("[v0] Creating billing document:", formData)
    onOpenChange(false)
    setFormData({
      delivery: "",
      billingDate: new Date().toISOString().split("T")[0],
      paymentTerms: "",
    })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Create Billing Document (VF01)</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="delivery">Delivery Document *</Label>
            <Select value={formData.delivery} onValueChange={(value) => setFormData({ ...formData, delivery: value })}>
              <SelectTrigger id="delivery">
                <SelectValue placeholder="Select delivery" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="DL-2024-001">DL-2024-001 - Tech Solutions Ltd</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="billingDate">Billing Date *</Label>
              <Input
                id="billingDate"
                type="date"
                value={formData.billingDate}
                onChange={(e) => setFormData({ ...formData, billingDate: e.target.value })}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="paymentTerms">Payment Terms *</Label>
              <Select
                value={formData.paymentTerms}
                onValueChange={(value) => setFormData({ ...formData, paymentTerms: value })}
              >
                <SelectTrigger id="paymentTerms">
                  <SelectValue placeholder="Select payment terms" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="net-30">Net 30</SelectItem>
                  <SelectItem value="net-60">Net 60</SelectItem>
                  <SelectItem value="net-90">Net 90</SelectItem>
                  <SelectItem value="immediate">Immediate Payment</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit">Create Billing Document</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
