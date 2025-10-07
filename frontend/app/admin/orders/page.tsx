import OrdersTable from "@/components/admin/orders-table"
import { getOrders, type OrderSummary } from "@/lib/dal"

export default async function SalesOrdersPage() {
  let orders: OrderSummary[] = []
  let error: string | null = null

  try {
    orders = await getOrders()
  } catch (err) {
    error = err instanceof Error ? err.message : "Failed to load orders"
  }

  return <OrdersTable initialOrders={orders} initialError={error} />
}
