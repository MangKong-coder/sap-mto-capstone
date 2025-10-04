"use client"

import { useState } from "react"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { DashboardHeader } from "@/components/dashboard-header"
import { Search, ArrowRight } from "lucide-react"
import { PlannedOrderTable } from "@/components/planned-order-table"
import { Input } from "@/components/ui/input"

export default function PlannedOrdersPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")

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

        <main className="p-6">
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <div>
                <h1 className="text-3xl font-bold text-foreground">Planned Orders</h1>
                <p className="text-sm text-muted-foreground mt-1">
                  Automatically generated from Sales Orders - Convert to Production Orders
                </p>
              </div>
            </div>
          </div>

          <div className="bg-card border border-border rounded-lg mb-6 p-4">
            <div className="flex items-center gap-3 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-blue-500" />
                <span className="text-muted-foreground">Sales Order Created</span>
              </div>
              <ArrowRight className="w-4 h-4 text-muted-foreground" />
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-yellow-500" />
                <span className="text-muted-foreground">Planned Order Generated</span>
              </div>
              <ArrowRight className="w-4 h-4 text-muted-foreground" />
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-purple-500" />
                <span className="text-muted-foreground">Convert to Production Order</span>
              </div>
            </div>
          </div>

          <div className="bg-card border border-border rounded-lg">
            <div className="p-4 border-b border-border">
              <div className="flex items-center gap-3">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Search by planned order number, sales order, or material..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
            </div>

            <PlannedOrderTable searchQuery={searchQuery} />
          </div>
        </main>
      </div>
    </div>
  )
}
