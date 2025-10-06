import { HomePageClient } from "@/components/home-page-client"
import { getProducts } from "@/lib/dal"

export default async function HomePage() {
  // Fetch products on the server side
  const products = await getProducts()

  return <HomePageClient products={products} />
}
