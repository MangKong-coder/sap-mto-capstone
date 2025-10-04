"use client"

import {
  LayoutDashboard,
  ShoppingCart,
  ClipboardList,
  Factory,
  CheckCircle,
  Truck,
  FileText,
  ChevronLeft,
  ChevronRight,
  Store,
} from "lucide-react"
import { cn } from "@/lib/utils"
import Link from "next/link"
import { usePathname } from "next/navigation"

interface DashboardSidebarProps {
  open: boolean
  onToggle: () => void
}

const menuItems = [
  { icon: LayoutDashboard, label: "Dashboard", href: "/" },
  { icon: ShoppingCart, label: "Merchandise Orders", href: "/sales-orders", badge: "VA01" },
  { icon: ClipboardList, label: "Planned Orders", href: "/planned-orders" },
  { icon: Factory, label: "Fulfillment Orders", href: "/production-orders", badge: "CO01" },
  { icon: CheckCircle, label: "Confirmations", href: "/confirmations" },
  { icon: Truck, label: "Deliveries", href: "/deliveries", badge: "VL01N" },
  { icon: FileText, label: "Billing", href: "/billing", badge: "VF01" },
]

export function DashboardSidebar({ open, onToggle }: DashboardSidebarProps) {
  const pathname = usePathname()

  return (
    <aside
      className={cn(
        "fixed left-0 top-0 h-screen bg-sidebar border-r border-sidebar-border transition-all duration-300 z-50",
        open ? "w-64" : "w-16",
      )}
    >
      <div className="flex items-center justify-between h-16 px-4 border-b border-sidebar-border">
        {open && (
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <Store className="w-5 h-5 text-primary-foreground" />
            </div>
            <div className="flex flex-col">
              <span className="font-semibold text-sidebar-foreground text-sm leading-tight">Mapua Bookstore</span>
              <span className="text-xs text-sidebar-foreground/60">Merchandise System</span>
            </div>
          </div>
        )}
        <button onClick={onToggle} className="p-1.5 rounded-md hover:bg-sidebar-accent text-sidebar-foreground">
          {open ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
        </button>
      </div>

      <nav className="p-3 space-y-1">
        {menuItems.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.label}
              href={item.href}
              className={cn(
                "w-full flex items-center gap-3 px-3 py-2.5 rounded-md transition-colors",
                isActive
                  ? "bg-sidebar-primary text-sidebar-primary-foreground"
                  : "text-sidebar-foreground hover:bg-sidebar-accent",
              )}
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              {open && (
                <div className="flex items-center justify-between flex-1">
                  <span className="text-sm font-medium">{item.label}</span>
                  {item.badge && (
                    <span className="text-xs px-1.5 py-0.5 rounded bg-sidebar-accent text-sidebar-foreground/70">
                      {item.badge}
                    </span>
                  )}
                </div>
              )}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
