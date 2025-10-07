"use client"

import { useState, useTransition } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Search, Play, CheckCircle } from "lucide-react"

import { OrderSummary } from "@/lib/dal"
import { SalesOrderStatus } from "@/lib/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  startProductionAction,
  markOrderReadyAction,
  updateOrderStatusAction,
  deleteOrderAction
} from "@/app/admin/orders/actions"

type OrdersTableProps = {
  initialOrders: OrderSummary[]
  initialError?: string | null
}

export default function OrdersTable({ initialOrders, initialError = null }: OrdersTableProps) {
  const router = useRouter()
  const [searchTerm, setSearchTerm] = useState("")
  const [actionError, setActionError] = useState<string | null>(initialError)
  const [actionSuccess, setActionSuccess] = useState<string | null>(null)
  const [pendingActions, setPendingActions] = useState<Set<number>>(new Set())
  const [isPending, startTransition] = useTransition()

  // Filter orders based on search term
  const filteredOrders = initialOrders.filter((order) => {
    const query = searchTerm.trim().toLowerCase()
    if (!query) return true

    const idMatches = order.id.toString().includes(query)
    const nameMatches = (order.customer_name ?? "").toLowerCase().includes(query)
    return idMatches || nameMatches
  })

  const handleStartProduction = async (orderId: number) => {
    setPendingActions(prev => new Set(prev).add(orderId))
    setActionError(null)
    setActionSuccess(null)

    startTransition(async () => {
      try {
        const result = await startProductionAction(orderId)
        if (result.success) {
          setActionSuccess(result.message)
          router.refresh() // Refresh to get updated data
        } else {
          setActionError(result.message)
        }
      } catch (error) {
        setActionError(error instanceof Error ? error.message : "Failed to start production")
      } finally {
        setPendingActions(prev => {
          const newSet = new Set(prev)
          newSet.delete(orderId)
          return newSet
        })
      }
    })
  }

  const handleMarkReady = async (orderId: number) => {
    setPendingActions(prev => new Set(prev).add(orderId))
    setActionError(null)
    setActionSuccess(null)

    startTransition(async () => {
      try {
        const result = await markOrderReadyAction(orderId)
        if (result.success) {
          setActionSuccess(result.message)
          router.refresh() // Refresh to get updated data
        } else {
          setActionError(result.message)
        }
      } catch (error) {
        setActionError(error instanceof Error ? error.message : "Failed to mark order ready for delivery")
      } finally {
        setPendingActions(prev => {
          const newSet = new Set(prev)
          newSet.delete(orderId)
          return newSet
        })
      }
    })
  }

  const getStatusColor = (status: SalesOrderStatus) => {
    switch (status) {
      case SalesOrderStatus.CREATED:
        return "bg-yellow-500/10 text-yellow-500"
      case SalesOrderStatus.IN_PRODUCTION:
        return "bg-blue-500/10 text-blue-500"
      case SalesOrderStatus.READY_FOR_DELIVERY:
        return "bg-purple-500/10 text-purple-500"
      case SalesOrderStatus.DELIVERED:
        return "bg-green-500/10 text-green-500"
      case SalesOrderStatus.BILLED:
        return "bg-emerald-500/10 text-emerald-500"
      case SalesOrderStatus.CANCELLED:
        return "bg-red-500/10 text-red-500"
      default:
        return "bg-zinc-500/10 text-zinc-500"
    }
  }

  const isPendingForOrder = (orderId: number) => pendingActions.has(orderId)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-zinc-900">Sales Orders</h2>
          <p className="text-sm text-zinc-600">Manage customer orders and production workflow</p>
        </div>
      </div>

      {actionError && <p className="text-sm text-red-600">{actionError}</p>}
      {actionSuccess && <p className="text-sm text-green-600">{actionSuccess}</p>}

      <Card className="border-zinc-200 bg-white">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-zinc-900">All Orders</CardTitle>
            <div className="relative w-64">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" />
              <Input
                placeholder="Search orders..."
                value={searchTerm}
                onChange={(event) => setSearchTerm(event.target.value)}
                className="border-zinc-300 bg-white pl-9 text-zinc-900 placeholder:text-zinc-400"
                disabled={isPending}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-200">
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Order ID</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Customer</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Date</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Total</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Status</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-600">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredOrders.length === 0 && (
                  <tr>
                    <td colSpan={6} className="py-6 text-center text-sm text-zinc-500">
                      No orders match your search.
                    </td>
                  </tr>
                )}
                {filteredOrders.map((order) => {
                  const formattedDate = order.created_at
                    ? new Date(order.created_at).toLocaleDateString()
                    : "--"
                  const isStartPending = isPendingForOrder(order.id)

                  return (
                    <tr key={order.id} className="border-b border-zinc-100">
                      <td className="py-4">
                        <Link href={`/orders/${order.id}`} className="text-sm font-medium text-red-500 hover:underline">
                          #{order.id}
                        </Link>
                      </td>
                      <td className="py-4 text-sm text-zinc-700">{order.customer_name ?? "Unknown"}</td>
                      <td className="py-4 text-sm text-zinc-600">{formattedDate}</td>
                      <td className="py-4 text-sm font-medium text-zinc-900">₱{order.total_amount.toFixed(2)}</td>
                      <td className="py-4">
                        <Badge variant="secondary" className={getStatusColor(order.status)}>
                          {order.status.replace(/_/g, " ")}
                        </Badge>
                      </td>
                      <td className="py-4 text-right">
                        <div className="flex justify-end gap-2">
                          {order.status === SalesOrderStatus.CREATED && (
                            <Button
                              size="sm"
                              onClick={() => handleStartProduction(order.id)}
                              className="bg-blue-500 text-white hover:bg-blue-600"
                              disabled={isStartPending}
                            >
                              <Play className="mr-1 h-3 w-3" />
                              {isStartPending ? "Starting..." : "Start Production"}
                            </Button>
                          )}
                          {order.status === SalesOrderStatus.IN_PRODUCTION && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleMarkReady(order.id)}
                              className="border-zinc-300 text-zinc-700 hover:bg-zinc-100"
                              disabled={isPendingForOrder(order.id)}
                            >
                              <CheckCircle className="mr-1 h-3 w-3" />
                              {isPendingForOrder(order.id) ? "Marking..." : "Mark Ready"}
                            </Button>
                          )}
                        </div>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
