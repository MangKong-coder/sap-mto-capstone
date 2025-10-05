"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Loader2 } from "lucide-react"
import { createOrder, getCustomers, getProducts, getWorkCenters, type Customer, type Product, type WorkCenter } from "@/lib/dal"
import { toast } from "sonner"

interface CreateSalesOrderDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onOrderCreated?: () => void
}

export function CreateSalesOrderDialog({ open, onOpenChange, onOrderCreated }: CreateSalesOrderDialogProps) {
  const [formData, setFormData] = useState({
    customer: "",
    customerType: "",
    material: "",
    quantity: "",
    deliveryDate: "",
    plant: "",
    priority: "Standard",
  })
  
  const [customers, setCustomers] = useState<Customer[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [workCenters, setWorkCenters] = useState<WorkCenter[]>([])
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  // Load customers and products when dialog opens
  useEffect(() => {
    if (open) {
      const loadData = async () => {
        setLoading(true)
        try {
          const [fetchedCustomers, fetchedProducts, fetchedWorkCenters] = await Promise.all([
            getCustomers(1, 100),
            getProducts(1, 100),
            getWorkCenters(1, 100)
          ])
          setCustomers(fetchedCustomers)
          setProducts(fetchedProducts)
          setWorkCenters(fetchedWorkCenters)
        } catch (error) {
          console.error('Failed to load data:', error)
          toast.error('Failed to load data for order creation')
        } finally {
          setLoading(false)
        }
      }
      loadData()
    }
  }, [open])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    
    try {
      // Validate required fields
      if (!formData.customerType) {
        throw new Error('Please select a customer type')
      }
      if (!formData.customer) {
        throw new Error('Please select a customer')
      }
      if (!formData.material) {
        throw new Error('Please select a product')
      }
      if (!formData.quantity || parseFloat(formData.quantity) <= 0) {
        throw new Error('Please enter a valid quantity')
      }
      if (!formData.deliveryDate) {
        throw new Error('Please select a delivery date')
      }
      if (!formData.plant) {
        throw new Error('Please select a work center')
      }

      const selectedCustomer = customers.find(c => c.id.toString() === formData.customer)
      const selectedProduct = products.find(p => p.id.toString() === formData.material)
      
      if (!selectedCustomer || !selectedProduct) {
        throw new Error('Invalid customer or product selection')
      }

      const selectedWorkCenter = workCenters.find(wc => wc.id.toString() === formData.plant)
      
      if (!selectedWorkCenter) {
        throw new Error('Invalid work center selection')
      }

      const orderData = {
        customer_id: selectedCustomer.id,
        delivery_date: formData.deliveryDate || undefined,
        priority: formData.priority.toUpperCase(),
        work_center_id: selectedWorkCenter.id,
        items: [
          {
            product_id: selectedProduct.id,
            quantity: parseFloat(formData.quantity),
            unit_price: selectedProduct.price,
          }
        ]
      }

      await createOrder(orderData)
      toast.success('Order created successfully!')
      
      // Reset form
      setFormData({
        customer: "",
        customerType: "",
        material: "",
        quantity: "",
        deliveryDate: "",
        plant: "",
        priority: "Standard",
      })
      
      onOpenChange(false)
      onOrderCreated?.()
      
    } catch (error) {
      console.error('Failed to create order:', error)
      toast.error(error instanceof Error ? error.message : 'Failed to create order')
    } finally {
      setSubmitting(false)
    }
  }

  const filteredCustomers = customers.filter(customer => {
    if (!formData.customerType) return true
    return formData.customerType === 'Department' 
      ? customer.customer_type === 'DEPARTMENT'
      : customer.customer_type === 'CAMPUS'
  })

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Create Merchandise Order (VA01)</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="customerType">Customer Type *</Label>
              <Select
                value={formData.customerType}
                onValueChange={(value) => setFormData({ ...formData, customerType: value, customer: "" })}
              >
                <SelectTrigger id="customerType">
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Department">Department</SelectItem>
                  <SelectItem value="Campus">Campus</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="customer">{formData.customerType === "Department" ? "Department" : "Campus"} *</Label>
              <Select
                value={formData.customer}
                onValueChange={(value) => setFormData({ ...formData, customer: value })}
                disabled={!formData.customerType || loading}
              >
                <SelectTrigger id="customer">
                  <SelectValue placeholder={loading ? "Loading..." : `Select ${formData.customerType || "customer"}`} />
                </SelectTrigger>
                <SelectContent>
                  {filteredCustomers.map((customer) => (
                    <SelectItem key={customer.id} value={customer.id.toString()}>
                      {customer.name}
                    </SelectItem>
                  ))}
                  {filteredCustomers.length === 0 && !loading && (
                    <SelectItem value="" disabled>
                      No {formData.customerType?.toLowerCase()}s available
                    </SelectItem>
                  )}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="material">School Merchandise *</Label>
            <Select 
              value={formData.material} 
              onValueChange={(value) => setFormData({ ...formData, material: value })}
              disabled={loading}
            >
              <SelectTrigger id="material">
                <SelectValue placeholder={loading ? "Loading products..." : "Select merchandise"} />
              </SelectTrigger>
              <SelectContent>
                {products.map((product) => (
                  <SelectItem key={product.id} value={product.id.toString()}>
                    {product.sku} - {product.name}
                  </SelectItem>
                ))}
                {products.length === 0 && !loading && (
                  <SelectItem value="" disabled>
                    No products available
                  </SelectItem>
                )}
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-3 gap-4">
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

            <div className="space-y-2">
              <Label htmlFor="priority">Priority *</Label>
              <Select
                value={formData.priority}
                onValueChange={(value) => setFormData({ ...formData, priority: value })}
              >
                <SelectTrigger id="priority">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Standard">Standard</SelectItem>
                  <SelectItem value="Urgent">Urgent</SelectItem>
                  <SelectItem value="Rush">Rush</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="plant">Work Center *</Label>
            <Select 
              value={formData.plant} 
              onValueChange={(value) => setFormData({ ...formData, plant: value })}
              disabled={loading}
            >
              <SelectTrigger id="plant">
                <SelectValue placeholder={loading ? "Loading work centers..." : "Select work center"} />
              </SelectTrigger>
              <SelectContent>
                {workCenters.map((workCenter) => (
                  <SelectItem key={workCenter.id} value={workCenter.id.toString()}>
                    {workCenter.name}
                  </SelectItem>
                ))}
                {workCenters.length === 0 && !loading && (
                  <SelectItem value="" disabled>
                    No work centers available
                  </SelectItem>
                )}
              </SelectContent>
            </Select>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)} disabled={submitting}>
              Cancel
            </Button>
            <Button type="submit" disabled={submitting || loading}>
              {submitting && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
              Create Merchandise Order
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
