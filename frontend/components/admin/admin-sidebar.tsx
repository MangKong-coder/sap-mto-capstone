"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { LayoutDashboard, ShoppingCart, Factory, Truck, FileText, Package, ChevronRight } from "lucide-react"
import { cn } from "@/lib/utils"

const navigation = [
  { name: "Dashboard", href: "/admin", icon: LayoutDashboard },
  { name: "Sales Orders", href: "/admin/orders", icon: ShoppingCart },
  { name: "Production", href: "/admin/production", icon: Factory },
  { name: "Deliveries", href: "/admin/deliveries", icon: Truck },
  { name: "Billings", href: "/admin/billings", icon: FileText },
  { name: "Products", href: "/admin/products", icon: Package },
]

export function AdminSidebar() {
  const pathname = usePathname()

  return (
    <aside className="flex w-64 flex-col border-r border-zinc-200 bg-white">
      <div className="flex h-14 items-center border-b border-zinc-200 px-6">
        <span className="text-lg font-bold text-zinc-900">Admin</span>
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive ? "bg-red-50 text-red-600" : "text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900",
              )}
            >
              <item.icon className="h-5 w-5" />
              {item.name}
              {isActive && <ChevronRight className="ml-auto h-4 w-4" />}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
