# API Endpoint Quick Reference

## Base URL
`http://localhost:8000/api/v1`

## Domain Groups

### 🔧 Components
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/components` | Add new component |
| PUT | `/components/{id}` | Update component |
| GET | `/components/{id}` | Get component by ID |
| GET | `/components/code/{part_code}` | Get by part code |
| GET | `/components/{id}/availability` | Check availability |
| GET | `/components` | List all (paginated) |

### 📊 Component Usage
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/component-usage` | Record usage |
| GET | `/component-usage/{id}` | Get by ID |
| GET | `/component-usage/work-order/{id}` | List by work order |
| GET | `/component-usage/component/{id}` | List by component |
| GET | `/component-usage/order/{id}/summary` | Order usage summary |
| GET | `/component-usage` | List all (paginated) |

### 👥 Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/customers` | Register customer |
| PUT | `/customers/{id}` | Update profile |
| GET | `/customers/{id}` | Get by ID |
| GET | `/customers/{id}/orders` | Get customer orders |
| GET | `/customers` | List all (paginated) |

### 📦 Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders` | Place new order |
| PUT | `/orders/{id}/cancel` | Cancel order |
| GET | `/orders/{id}` | Get by ID |
| GET | `/orders/{id}/status` | Get full status |
| GET | `/orders/{id}/planned-orders` | List planned orders |
| GET | `/orders/{id}/deliveries` | List deliveries |
| GET | `/orders/{id}/invoices` | List invoices |
| GET | `/orders/customer/{id}` | List by customer |
| GET | `/orders` | List all (paginated) |

### 📋 Planned Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/planned-orders` | Generate planned order |
| PUT | `/planned-orders/{id}` | Update details |
| PUT | `/planned-orders/{id}/convert` | Convert to work order |
| GET | `/planned-orders/{id}` | Get by ID |
| GET | `/planned-orders` | List all (paginated) |

### 🏭 Work Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/work-orders/{id}/start` | Start work order |
| PUT | `/work-orders/{id}/confirm` | Confirm completion |
| PUT | `/work-orders/{id}/consume` | Consume components |
| PUT | `/work-orders/{id}/close` | Close work order |
| GET | `/work-orders/{id}` | Get by ID |
| GET | `/work-orders/{id}/usage` | Get component usage |
| GET | `/work-orders` | List all (paginated) |

### 🚚 Deliveries
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/deliveries` | Schedule delivery |
| PUT | `/deliveries/{id}/status` | Update status |
| GET | `/deliveries/{id}` | Get by ID |
| GET | `/deliveries/customer/{id}` | List by customer |
| GET | `/deliveries/order/{id}` | List by order |
| GET | `/deliveries` | List all (paginated) |

### 🧾 Invoices
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/invoices` | Generate invoice |
| PUT | `/invoices/{id}/pay` | Mark as paid |
| PUT | `/invoices/{id}/post` | Post invoice |
| PUT | `/invoices/{id}/cancel` | Cancel invoice |
| GET | `/invoices/{id}` | Get by ID |
| GET | `/invoices/customer/{id}/outstanding` | Unpaid invoices |
| GET | `/invoices/order/{id}` | List by order |
| GET | `/invoices` | List all (paginated) |

### 🛍️ Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products` | Add new product |
| PUT | `/products/{id}` | Update details |
| GET | `/products/{id}` | Get by ID |
| GET | `/products/sku/{sku}` | Get by SKU |
| GET | `/products/{id}/availability` | Check availability |
| GET | `/products` | List all (paginated) |

### 📈 Reporting
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reporting/orders/{id}/flow` | Full order flow trace |
| GET | `/reporting/production-status` | Production summary |
| GET | `/reporting/component-consumption` | Component usage aggregate |
| GET | `/reporting/orders/{id}/component-usage` | Order component usage |
| GET | `/reporting/customers/{id}/summary` | Customer summary |
| GET | `/reporting/orders/summary` | Order summary |

### 🔄 MTO Flow
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mto/auto-production-order` | Auto-create production |

## Pagination
All list endpoints support:
- `?page=1` (default: 1)
- `?size=20` (default: 20, max: 100)

Example: `/api/v1/orders?page=2&size=50`

## HTTP Status Codes
- `200` OK - Successful GET/PUT
- `201` Created - Successful POST
- `400` Bad Request - Validation error
- `404` Not Found - Entity not found
- `409` Conflict - Business rule violation

## Complete End-to-End Flow

### 1. Setup Data
```bash
# Create customer
POST /customers
{
  "name": "Acme Corp",
  "email": "orders@acme.com",
  "phone": "+1234567890"
}

# Create product
POST /products
{
  "sku": "WIDGET-001",
  "name": "Premium Widget",
  "price": 99.99
}

# Create components
POST /components
{
  "part_code": "STEEL-001",
  "name": "Steel Plate",
  "cost": 15.50
}
```

### 2. Order → Production Flow
```bash
# Place order
POST /orders
{
  "customer_id": 1,
  "items": [{"product_id": 1, "quantity": 10}]
}

# Auto-generate planned orders
POST /mto/auto-production-order
{
  "order_id": 1
}

# Convert to work order
PUT /planned-orders/1/convert

# Start production
PUT /work-orders/1/start

# Consume components
PUT /work-orders/1/consume
{
  "components": [{"component_id": 1, "quantity": 5}]
}

# Confirm completion
PUT /work-orders/1/confirm
{
  "produced_qty": 10
}
```

### 3. Delivery & Billing
```bash
# Schedule delivery
POST /deliveries
{
  "order_id": 1,
  "quantity": 10
}

# Update delivery status
PUT /deliveries/1/status
{
  "status": "SHIPPED"
}

# Generate invoice
POST /invoices
{
  "order_id": 1,
  "total_amount": 999.90
}

# Post invoice
PUT /invoices/1/post

# Mark as paid
PUT /invoices/1/pay
```

### 4. Reporting
```bash
# Get full order flow
GET /reporting/orders/1/flow

# Get production status
GET /reporting/production-status

# Get component consumption
GET /reporting/component-consumption
```

## Interactive Documentation
Visit: http://localhost:8000/docs
