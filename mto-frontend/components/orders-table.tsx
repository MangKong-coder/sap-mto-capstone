"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ExternalLink } from "lucide-react"

const orders = [
  {
    id: "SO-4500012345",
    customer: "Acme Corporation",
    product: "Custom Widget A",
    quantity: 500,
    status: "Production Confirmed",
    statusColor: "bg-chart-2 text-chart-2",
    dueDate: "2024-02-15",
    progress: 85,
    productionOrder: "PR-7000456",
  },
  {
    id: "SO-4500012346",
    customer: "TechStart Inc",
    product: "Industrial Component B",
    quantity: 250,
    status: "Planned Order Created",
    statusColor: "bg-chart-3 text-chart-3",
    dueDate: "2024-02-18",
    progress: 30,
    productionOrder: "PO-1000124",
  },
  {
    id: "SO-4500012347",
    customer: "Global Manufacturing",
    product: "Precision Part C",
    quantity: 1000,
    status: "Ready for Delivery",
    statusColor: "bg-chart-5 text-chart-5",
    dueDate: "2024-02-12",
    progress: 95,
    productionOrder: "PR-7000458",
  },
  {
    id: "SO-4500012348",
    customer: "Innovation Labs",
    product: "Custom Assembly D",
    quantity: 150,
    status: "Billing Complete",
    statusColor: "bg-success text-success",
    dueDate: "2024-02-10",
    progress: 100,
    productionOrder: "PR-7000459",
  },
  {
    id: "SO-4500012349",
    customer: "Enterprise Solutions",
    product: "Specialized Unit E",
    quantity: 750,
    status: "Sales Order Created",
    statusColor: "bg-chart-1 text-chart-1",
    dueDate: "2024-02-20",
    progress: 10,
    productionOrder: "-",
  },
]

export function OrdersTable() {
  return (
    <Card className="p-6 bg-card border-border">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-card-foreground">Sales Orders (VA01)</h3>
          <p className="text-sm text-muted-foreground">Track MTO order progression and document linkage</p>
        </div>
        <Button variant="outline" size="sm">
          View All Orders
        </Button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Sales Order</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Customer</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Product</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Quantity</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Prod. Order</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Status</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Due Date</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Progress</th>
              <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground"></th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id} className="border-b border-border hover:bg-accent/50 transition-colors">
                <td className="py-4 px-4">
                  <span className="font-mono text-sm text-card-foreground">{order.id}</span>
                </td>
                <td className="py-4 px-4">
                  <span className="text-sm text-card-foreground">{order.customer}</span>
                </td>
                <td className="py-4 px-4">
                  <span className="text-sm text-card-foreground">{order.product}</span>
                </td>
                <td className="py-4 px-4">
                  <span className="text-sm text-card-foreground">{order.quantity}</span>
                </td>
                <td className="py-4 px-4">
                  <span className="font-mono text-sm text-muted-foreground">{order.productionOrder}</span>
                </td>
                <td className="py-4 px-4">
                  <Badge variant="secondary" className={`${order.statusColor} bg-opacity-10`}>
                    {order.status}
                  </Badge>
                </td>
                <td className="py-4 px-4">
                  <span className="text-sm text-card-foreground">{order.dueDate}</span>
                </td>
                <td className="py-4 px-4">
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden min-w-[60px]">
                      <div className="h-full bg-chart-1 transition-all" style={{ width: `${order.progress}%` }} />
                    </div>
                    <span className="text-sm text-muted-foreground w-10 text-right">{order.progress}%</span>
                  </div>
                </td>
                <td className="py-4 px-4">
                  <Button variant="ghost" size="icon" title="View document flow">
                    <ExternalLink className="w-4 h-4" />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}
