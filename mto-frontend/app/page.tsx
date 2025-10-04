"use client"

import { useState } from "react"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { DashboardHeader } from "@/components/dashboard-header"
import { MetricsGrid } from "@/components/metrics-grid"
import { OrdersChart } from "@/components/orders-chart"
import { MTOProcessFlow } from "@/components/mto-process-flow"
import { RecentOrdersTable } from "@/components/recent-orders-table"
import { ResourceUtilization } from "@/components/resource-utilization"

export default function MTODashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="min-h-screen bg-background">
      <DashboardSidebar open={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      <div
        className="transition-all duration-300"
        style={{
          marginLeft: sidebarOpen ? "16rem" : "4rem",
        }}
      >
        <DashboardHeader />

        <main className="p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-foreground">Mapua Bookstore Dashboard</h1>
              <p className="text-muted-foreground mt-1">School Merchandise MTO Flow - Department & Campus Orders</p>
            </div>
          </div>

          <MetricsGrid />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <OrdersChart />
            <ResourceUtilization />
          </div>

          <MTOProcessFlow />

          <RecentOrdersTable />
        </main>
      </div>
    </div>
  )
}
