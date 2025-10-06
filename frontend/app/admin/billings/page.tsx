"use client"

import { useOrdersStore } from "@/lib/orders-store"
import { useAdminStore } from "@/lib/admin-store"
import { SalesOrderStatus } from "@/lib/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { FileText } from "lucide-react"
import Link from "next/link"

export default function BillingsPage() {
  const { orders, billings } = useOrdersStore()
  const { createBilling } = useAdminStore()

  const getOrderDetails = (salesOrderId: number) => {
    return orders.find((o) => o.id === salesOrderId)
  }

  const deliveredOrders = orders.filter(
    (o) => o.status === SalesOrderStatus.DELIVERED && !billings.find((b) => b.sales_order_id === o.id),
  )

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-zinc-900">Billings</h2>
        <p className="text-sm text-zinc-600">Manage invoices and billing records</p>
      </div>

      {/* Pending Billings */}
      {deliveredOrders.length > 0 && (
        <Card className="border-zinc-200 bg-white">
          <CardHeader>
            <CardTitle className="text-zinc-900">Pending Billings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-zinc-200">
                    <th className="pb-3 text-left text-sm font-medium text-zinc-600">Order ID</th>
                    <th className="pb-3 text-left text-sm font-medium text-zinc-600">Customer</th>
                    <th className="pb-3 text-right text-sm font-medium text-zinc-600">Amount</th>
                    <th className="pb-3 text-left text-sm font-medium text-zinc-600">Delivered Date</th>
                    <th className="pb-3 text-right text-sm font-medium text-zinc-600">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {deliveredOrders.map((order) => (
                    <tr key={order.id} className="border-b border-zinc-100">
                      <td className="py-4">
                        <Link href={`/orders/${order.id}`} className="text-sm text-red-500 hover:underline">
                          #{order.id}
                        </Link>
                      </td>
                      <td className="py-4 text-sm text-zinc-700">Customer {order.customer_id}</td>
                      <td className="py-4 text-right text-sm font-medium text-zinc-900">
                        ₱{order.total_amount.toFixed(2)}
                      </td>
                      <td className="py-4 text-sm text-zinc-600">{new Date(order.created_at).toLocaleDateString()}</td>
                      <td className="py-4 text-right">
                        <Button
                          size="sm"
                          onClick={() => createBilling(order.id)}
                          className="bg-green-500 text-white hover:bg-green-600"
                        >
                          <FileText className="mr-1 h-3 w-3" />
                          Generate Invoice
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* All Billings */}
      <Card className="border-zinc-200 bg-white">
        <CardHeader>
          <CardTitle className="text-zinc-900">All Billings</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-200">
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Billing ID</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Sales Order</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Invoice Number</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-600">Amount</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Billing Date</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Status</th>
                </tr>
              </thead>
              <tbody>
                {billings.map((billing) => {
                  const order = getOrderDetails(billing.sales_order_id)
                  return (
                    <tr key={billing.id} className="border-b border-zinc-100">
                      <td className="py-4 text-sm font-medium text-zinc-900">BILL-{billing.id}</td>
                      <td className="py-4">
                        <Link
                          href={`/orders/${billing.sales_order_id}`}
                          className="text-sm text-red-500 hover:underline"
                        >
                          #{billing.sales_order_id}
                        </Link>
                      </td>
                      <td className="py-4 text-sm text-zinc-700">{billing.invoice_number}</td>
                      <td className="py-4 text-right text-sm font-medium text-zinc-900">₱{billing.amount.toFixed(2)}</td>
                      <td className="py-4 text-sm text-zinc-600">
                        {new Date(billing.billed_date).toLocaleDateString()}
                      </td>
                      <td className="py-4">
                        <Badge variant="secondary" className="bg-green-100 text-green-700">
                          Billed
                        </Badge>
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
