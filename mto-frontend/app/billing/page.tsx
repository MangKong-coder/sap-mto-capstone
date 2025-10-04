"use client"

import { useState } from "react"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { DashboardHeader } from "@/components/dashboard-header"
import { Button } from "@/components/ui/button"
import { Plus, Search, Filter } from "lucide-react"
import { BillingTable } from "@/components/billing-table"
import { CreateBillingDialog } from "@/components/create-billing-dialog"
import { Input } from "@/components/ui/input"

export default function BillingPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [createDialogOpen, setCreateDialogOpen] = useState(false)
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
                <h1 className="text-3xl font-bold text-foreground">Billing Documents</h1>
                <p className="text-sm text-muted-foreground mt-1">Transaction Code: VF01 - Create Billing Document</p>
              </div>
              <Button onClick={() => setCreateDialogOpen(true)} className="gap-2">
                <Plus className="w-4 h-4" />
                Create Billing
              </Button>
            </div>
          </div>

          <div className="bg-card border border-border rounded-lg">
            <div className="p-4 border-b border-border">
              <div className="flex items-center gap-3">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Search by billing number, customer, or sales order..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Button variant="outline" className="gap-2 bg-transparent">
                  <Filter className="w-4 h-4" />
                  Filter
                </Button>
              </div>
            </div>

            <BillingTable searchQuery={searchQuery} />
          </div>
        </main>
      </div>

      <CreateBillingDialog open={createDialogOpen} onOpenChange={setCreateDialogOpen} />
    </div>
  )
}
