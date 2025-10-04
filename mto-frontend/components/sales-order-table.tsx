"use client"

import { useState, useEffect } from "react"
import { getOrders } from "@/lib/dal"
import type { SalesOrder } from "@/lib/types"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Eye, FileText, Loader2, AlertTriangle } from "lucide-react"
import { SalesOrderDetailsDialog } from "./sales-order-details-dialog"

interface SalesOrderTableProps {
  searchQuery: string
  refreshKey?: number
}

export function SalesOrderTable({ searchQuery, refreshKey }: SalesOrderTableProps) {
  const [orders, setOrders] = useState<SalesOrder[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [selectedOrder, setSelectedOrder] = useState<SalesOrder | null>(null)
  const [detailsOpen, setDetailsOpen] = useState(false)

  // Fetch orders from backend
  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true)
        setError(null)
        const fetchedOrders = await getOrders(currentPage, 20)
        setOrders(fetchedOrders)
      } catch (err) {
        console.error('Failed to fetch orders:', err)
        setError(err instanceof Error ? err.message : 'Failed to fetch orders')
      } finally {
        setLoading(false)
      }
    }

    fetchOrders()
  }, [currentPage, refreshKey])

  const filteredOrders = orders.filter(
    (order) =>
      order.orderNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.customer.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.material.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  const getStatusColor = (status: SalesOrder["status"]) => {
    switch (status) {
      case "Open":
        return "bg-blue-500/10 text-blue-500 border-blue-500/20"
      case "In Planning":
        return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
      case "In Production":
        return "bg-purple-500/10 text-purple-500 border-purple-500/20"
      case "Delivered":
        return "bg-green-500/10 text-green-500 border-green-500/20"
      case "Billed":
        return "bg-gray-500/10 text-gray-500 border-gray-500/20"
      default:
        return "bg-gray-500/10 text-gray-500 border-gray-500/20"
    }
  }

  const handleViewDetails = (order: SalesOrder) => {
    setSelectedOrder(order)
    setDetailsOpen(true)
  }

  // Loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="flex items-center gap-2">
          <Loader2 className="w-5 h-5 animate-spin" />
          <span>Loading orders...</span>
        </div>
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="flex items-center gap-2 text-destructive">
          <AlertTriangle className="w-5 h-5" />
          <span>{error}</span>
        </div>
      </div>
    )
  }

  return (
    <>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-muted/50 border-b border-border">
            <tr>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Order Number</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Customer</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Material</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Quantity</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Delivery Date</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Net Value</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Status</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredOrders.length === 0 ? (
              <tr>
                <td colSpan={8} className="p-8 text-center text-muted-foreground">
                  {searchQuery ? 'No orders found matching your search.' : 'No orders found.'}
                </td>
              </tr>
            ) : (
              filteredOrders.map((order) => (
                <tr key={order.id} className="border-b border-border hover:bg-muted/30 transition-colors">
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4 text-primary" />
                      <span className="font-medium text-foreground">{order.orderNumber}</span>
                    </div>
                  </td>
                  <td className="p-4 text-foreground">{order.customer}</td>
                  <td className="p-4 text-foreground">{order.material}</td>
                  <td className="p-4 text-foreground">{order.quantity}</td>
                  <td className="p-4 text-foreground">{new Date(order.deliveryDate).toLocaleDateString()}</td>
                  <td className="p-4 text-foreground">${order.netValue.toLocaleString()}</td>
                  <td className="p-4">
                    <Badge variant="outline" className={getStatusColor(order.status)}>
                      {order.status}
                    </Badge>
                  </td>
                  <td className="p-4">
                    <Button variant="ghost" size="sm" onClick={() => handleViewDetails(order)} className="gap-2">
                      <Eye className="w-4 h-4" />
                      View
                    </Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {selectedOrder && (
        <SalesOrderDetailsDialog order={selectedOrder} open={detailsOpen} onOpenChange={setDetailsOpen} />
      )}
    </>
  )
}
