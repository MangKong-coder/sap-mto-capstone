# MTO Backend

Make-to-Order (MTO) Manufacturing Flow Backend API built with FastAPI.

## Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure Environment

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials.

### 3. Set up PostgreSQL

Make sure PostgreSQL is running and create the database:

```sql
CREATE DATABASE mto_db;
```

### 4. Run Migrations

Initialize the database schema:

```bash
# Create initial migration
uv run alembic revision --autogenerate -m "Initial migration"

# Apply migrations
uv run alembic upgrade head
```

Or create tables directly (for development):

```bash
uv run python scripts/create_db.py
```

## Running the Server

Start the development server:

```bash
uv run main.py
```

Or with uvicorn directly:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## Project Structure

```
mto-backend/
├── app/
│   ├── api/
│   │   ├── v1/           # API routes (sales_orders, production_orders, deliveries, users)
│   │   └── deps.py       # API dependencies
│   ├── core/             # Core configuration (config, security, logging)
│   ├── crud/             # Database operations
│   ├── db/               # Database setup (session, base, init)
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic (mto_flow, reporting)
│   └── main.py           # FastAPI application
├── alembic/              # Database migrations
├── scripts/              # Utility scripts
├── main.py               # Entry point
├── pyproject.toml        # Dependencies
└── .env                  # Environment variables (not in git)
```

## API Endpoints

### Sales Orders
- `POST /api/v1/sales-orders/` - Create sales order
- `GET /api/v1/sales-orders/` - List sales orders
- `GET /api/v1/sales-orders/{id}` - Get sales order
- `PATCH /api/v1/sales-orders/{id}` - Update sales order
- `DELETE /api/v1/sales-orders/{id}` - Delete sales order

### Production Orders
- `POST /api/v1/production-orders/` - Create production order
- `GET /api/v1/production-orders/` - List production orders
- `GET /api/v1/production-orders/{id}` - Get production order
- `PATCH /api/v1/production-orders/{id}` - Update production order
- `DELETE /api/v1/production-orders/{id}` - Delete production order

### Deliveries
- `POST /api/v1/deliveries/` - Create delivery
- `GET /api/v1/deliveries/` - List deliveries
- `GET /api/v1/deliveries/{id}` - Get delivery
- `PATCH /api/v1/deliveries/{id}` - Update delivery
- `DELETE /api/v1/deliveries/{id}` - Delete delivery

### Users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/` - List users
- `GET /api/v1/users/{id}` - Get user
- `PATCH /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Development

### Create a new migration

```bash
uv run alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
uv run alembic upgrade head
```

### Rollback migrations

```bash
uv run alembic downgrade -1
```


