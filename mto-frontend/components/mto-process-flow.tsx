"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowRight, FileText, ClipboardList, Cog, Package, DollarSign, CheckCircle2 } from "lucide-react"
import { mockSalesOrders, mockProductionOrders, mockDeliveries, mockBillings } from "@/lib/mock-data"

export function MTOProcessFlow() {
  const processStages = [
    {
      name: "Sales Order",
      transaction: "VA01",
      count: mockSalesOrders.filter((o) => o.status === "Open" || o.status === "In Planning").length,
      icon: FileText,
      color: "bg-blue-500/10",
      textColor: "text-blue-500",
      description: "Customer order creation",
    },
    {
      name: "Planned Order",
      transaction: "MD11",
      count: mockSalesOrders.filter((o) => o.status === "In Planning").length,
      icon: ClipboardList,
      color: "bg-yellow-500/10",
      textColor: "text-yellow-500",
      description: "Auto-generated from SO",
    },
    {
      name: "Production Order",
      transaction: "CO01",
      count: mockProductionOrders.filter((o) => o.status === "Released" || o.status === "In Progress").length,
      icon: Cog,
      color: "bg-purple-500/10",
      textColor: "text-purple-500",
      description: "Converted & confirmed",
    },
    {
      name: "Delivery",
      transaction: "VL01N",
      count: mockDeliveries.filter((d) => d.status === "Completed").length,
      icon: Package,
      color: "bg-green-500/10",
      textColor: "text-green-500",
      description: "Goods issue posted",
    },
    {
      name: "Billing",
      transaction: "VF01",
      count: mockBillings.length,
      icon: DollarSign,
      color: "bg-emerald-500/10",
      textColor: "text-emerald-500",
      description: "Invoice created",
    },
  ]

  const recentFlows = mockSalesOrders.slice(0, 5).map((so) => {
    const prodOrder = mockProductionOrders.find((po) => po.salesOrder === so.orderNumber)
    const delivery = mockDeliveries.find((d) => d.salesOrder === so.orderNumber)
    const billing = mockBillings.find((b) => b.salesOrder === so.orderNumber)

    return {
      salesOrder: so.orderNumber,
      plannedOrder: prodOrder ? `PO-${prodOrder.orderNumber.slice(-6)}` : "-",
      productionOrder: prodOrder?.orderNumber || "-",
      delivery: delivery?.deliveryNumber || "-",
      billing: billing?.billingNumber || "-",
      customer: so.customer,
      status: so.status,
      statusColor:
        so.status === "Delivered" || so.status === "Billed"
          ? "green-500"
          : so.status === "In Production"
            ? "purple-500"
            : so.status === "In Planning"
              ? "yellow-500"
              : "blue-500",
    }
  })

  return (
    <div className="space-y-6">
      {/* Process Flow Visualization */}
      <Card className="p-6">
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-foreground">MTO Process Flow</h3>
          <p className="text-sm text-muted-foreground">Sales order to billing cycle - PP/SD integration</p>
        </div>

        <div className="flex items-center gap-3 overflow-x-auto pb-2">
          {processStages.map((stage, index) => (
            <div key={stage.name} className="flex items-center gap-3">
              <div className="flex-shrink-0 min-w-[200px]">
                <div className="p-4 rounded-lg bg-muted border border-border hover:border-primary/50 transition-colors">
                  <div className="flex items-center gap-3 mb-3">
                    <div className={`p-2 rounded-lg ${stage.color}`}>
                      <stage.icon className={`w-5 h-5 ${stage.textColor}`} />
                    </div>
                    <div className="flex-1">
                      <div className="font-semibold text-foreground text-sm">{stage.name}</div>
                      <div className="text-xs text-muted-foreground font-mono">{stage.transaction}</div>
                    </div>
                  </div>
                  <div className="text-xs text-muted-foreground mb-2">{stage.description}</div>
                  <div className="flex items-baseline gap-2">
                    <span className="text-2xl font-bold text-foreground">{stage.count}</span>
                    <span className="text-xs text-muted-foreground">active</span>
                  </div>
                </div>
              </div>
              {index < processStages.length - 1 && (
                <ArrowRight className="w-5 h-5 text-muted-foreground flex-shrink-0" />
              )}
            </div>
          ))}
        </div>
      </Card>

      {/* Order Linkage Table */}
      <Card className="p-6">
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-foreground">Sales Order to Production Order Linkage</h3>
          <p className="text-sm text-muted-foreground">Track document flow across PP and SD modules</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Sales Order</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Planned Order</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Production Order</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Delivery</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Billing</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Customer</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Status</th>
              </tr>
            </thead>
            <tbody>
              {recentFlows.map((flow) => (
                <tr key={flow.salesOrder} className="border-b border-border hover:bg-muted/50 transition-colors">
                  <td className="py-4 px-4">
                    <span className="font-mono text-sm text-foreground">{flow.salesOrder}</span>
                  </td>
                  <td className="py-4 px-4">
                    <span className="font-mono text-sm text-foreground">{flow.plannedOrder}</span>
                  </td>
                  <td className="py-4 px-4">
                    <span className="font-mono text-sm text-foreground">{flow.productionOrder}</span>
                  </td>
                  <td className="py-4 px-4">
                    <span className="font-mono text-sm text-muted-foreground">{flow.delivery}</span>
                  </td>
                  <td className="py-4 px-4">
                    <span className="font-mono text-sm text-muted-foreground">{flow.billing}</span>
                  </td>
                  <td className="py-4 px-4">
                    <span className="text-sm text-foreground">{flow.customer}</span>
                  </td>
                  <td className="py-4 px-4">
                    <Badge
                      variant="outline"
                      className={`bg-${flow.statusColor}/10 text-${flow.statusColor} border-${flow.statusColor}/20`}
                    >
                      {(flow.status === "Delivered" || flow.status === "Billed") && (
                        <CheckCircle2 className="w-3 h-3 mr-1" />
                      )}
                      {flow.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
