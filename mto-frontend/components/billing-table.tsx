"use client"

import { useState } from "react"
import { mockBillings } from "@/lib/mock-data"
import type { Billing } from "@/lib/types"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Eye, FileText, Download } from "lucide-react"

interface BillingTableProps {
  searchQuery: string
}

export function BillingTable({ searchQuery }: BillingTableProps) {
  const [billings] = useState<Billing[]>(mockBillings)

  const filteredBillings = billings.filter(
    (billing) =>
      billing.billingNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      billing.customer.toLowerCase().includes(searchQuery.toLowerCase()) ||
      billing.salesOrderNumber.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  const getStatusColor = (status: Billing["status"]) => {
    switch (status) {
      case "Created":
        return "bg-blue-500/10 text-blue-500 border-blue-500/20"
      case "Posted":
        return "bg-green-500/10 text-green-500 border-green-500/20"
      case "Paid":
        return "bg-emerald-500/10 text-emerald-500 border-emerald-500/20"
      case "Cancelled":
        return "bg-red-500/10 text-red-500 border-red-500/20"
      default:
        return "bg-gray-500/10 text-gray-500 border-gray-500/20"
    }
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead className="bg-muted/50 border-b border-border">
          <tr>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Billing Number</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Sales Order</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Delivery</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Customer</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Billing Date</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Net Value</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Payment Terms</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Status</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredBillings.map((billing) => (
            <tr key={billing.id} className="border-b border-border hover:bg-muted/30 transition-colors">
              <td className="p-4">
                <div className="flex items-center gap-2">
                  <FileText className="w-4 h-4 text-blue-500" />
                  <span className="font-medium text-foreground">{billing.billingNumber}</span>
                </div>
              </td>
              <td className="p-4">
                <span className="text-primary font-medium">{billing.salesOrderNumber}</span>
              </td>
              <td className="p-4 text-foreground">{billing.deliveryNumber}</td>
              <td className="p-4 text-foreground">{billing.customer}</td>
              <td className="p-4 text-foreground">{new Date(billing.billingDate).toLocaleDateString()}</td>
              <td className="p-4">
                <span className="font-semibold text-foreground">${billing.netValue.toLocaleString()}</span>
              </td>
              <td className="p-4 text-foreground">{billing.paymentTerms}</td>
              <td className="p-4">
                <Badge variant="outline" className={getStatusColor(billing.status)}>
                  {billing.status}
                </Badge>
              </td>
              <td className="p-4">
                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="sm" className="gap-2">
                    <Eye className="w-4 h-4" />
                    View
                  </Button>
                  <Button variant="ghost" size="sm" className="gap-2">
                    <Download className="w-4 h-4" />
                    PDF
                  </Button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
