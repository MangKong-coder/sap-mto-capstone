Perfect 👍 no tests for now, just a **clean scaffold** you can run right away.
Here’s the **step-by-step setup** with the commands.

---

# 📂 Backend Project Setup – Folder Structure (No Tests)

## 1. Initialize the Project

```bash
# Create project folder
mkdir backend && cd backend

# Initialize Python project (creates pyproject.toml)
uv init --package
```

---

## 2. Install Dependencies

```bash
# Core backend dependencies
uv add fastapi uvicorn[standard] sqlmodel psycopg2-binary alembic pydantic-settings python-multipart
```

---

## 3. Create Folder Structure

```bash
# App source folder
mkdir app

# API routers
mkdir -p app/api/v1

# Core settings & security
mkdir app/core

# CRUD logic
mkdir app/crud

# Database setup
mkdir app/db

# Schemas
mkdir app/schemas

# Services (business logic)
mkdir app/services

# Alembic migrations
mkdir alembic
mkdir alembic/versions

# Scripts
mkdir scripts
```

---

## 4. Create Base Files

```bash
# FastAPI entrypoint
touch app/main.py

# API dependency injection
touch app/api/deps.py

# Routers
touch app/api/v1/sales_orders.py
touch app/api/v1/production_orders.py
touch app/api/v1/deliveries.py
touch app/api/v1/users.py

# Core config & logging
touch app/core/config.py
touch app/core/security.py
touch app/core/logging.py

# CRUD files
touch app/crud/sales_orders.py
touch app/crud/production_orders.py
touch app/crud/deliveries.py
touch app/crud/users.py

# DB setup
touch app/db/session.py
touch app/db/init_db.py

# Models (single file)
touch app/models.py

# Schemas
touch app/schemas/sales_order.py
touch app/schemas/production_order.py
touch app/schemas/delivery.py
touch app/schemas/user.py

# Services
touch app/services/mto_flow.py
touch app/services/reporting.py

# Init files
touch app/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/core/__init__.py
touch app/crud/__init__.py
touch app/db/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
```

---

## 5. Alembic Setup

```bash
# Initialize alembic migrations
alembic init alembic
```

This will create:

* `alembic/env.py`
* `alembic.ini`
* `alembic/versions/`

---

## 6. Environment Configuration

Create a `.env` file in the backend directory with:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/mto_db
```

The `config.py` will read `DATABASE_URL` directly from this `.env` file.

---

## 7. Final Project Tree

```bash
backend/
│── alembic/
│   ├── versions/
│   └── env.py
│── app/
│   ├── api/v1/
│   │   ├── sales_orders.py
│   │   ├── production_orders.py
│   │   ├── deliveries.py
│   │   └── users.py
│   ├── core/
│   ├── crud/
│   ├── db/
│   ├── schemas/
│   ├── services/
│   ├── models.py
│   ├── main.py
│   └── __init__.py
│── scripts/
│── alembic.ini
│── pyproject.toml
```

---

Do you want me to also **pre-fill `main.py`, `config.py`, and `session.py` with starter code** so the backend actually runs right after this scaffold?
