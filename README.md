# SAP MTO Capstone Project

Make-to-Order (MTO) system for managing sales orders, production, delivery, and billing workflows.
Developed by James Kerby D. Domingo - 2025102635, for the capstone project of his team, CORES, Elisha Avila, Andrea Baladad, Rufamel Gascon, and Nichole Teodoro, in CSS100.

## Project Structure

```
sap-mto-capstone/
├── backend/          # FastAPI backend
└── frontend/         # Next.js frontend
```

## Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 18+** and **npm** (for frontend)
- **PostgreSQL** (or SQLite for development)

### Installing Prerequisites

**Python:**
- Download from [python.org](https://www.python.org/downloads/)
- Verify installation: `python --version` or `python3 --version`

**Node.js and npm:**
- Download from [nodejs.org](https://nodejs.org/) (npm is included with Node.js)
- Verify installation: `node --version` and `npm --version`

**PostgreSQL (optional):**
- Download from [postgresql.org](https://www.postgresql.org/download/)
- Or use SQLite (no installation needed, included with Python)

## Backend Setup

### 1. Navigate to backend directory

```bash
cd backend
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**Note:** This will automatically install uvicorn (the ASGI server) along with all other backend dependencies including FastAPI, SQLModel, etc.

### 4. Configure environment variables

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mto_db
# Or for SQLite: DATABASE_URL=sqlite:///./mapua_mto.db

PUBLIC_APP_URL=http://localhost:3000
RESEND_API_KEY=your_resend_api_key_here
```

### 5. Initialize the database

The database will be automatically initialized on first run. Tables are created based on SQLModel models.

### 6. Run the backend server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at: **http://localhost:8000**

API documentation: **http://localhost:8000/docs**

## Frontend Setup

### 1. Navigate to frontend directory

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

**Note:** This will install all frontend dependencies including Next.js, React, TypeScript, Tailwind CSS, and all UI libraries listed in `package.json`.

### 3. Configure environment variables

Create a `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BACKEND_API_URL=http://localhost:8000
```

### 4. Run the development server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:3000**

## Running Both Apps

### Option 1: Two Terminal Windows

**Terminal 1 (Backend):**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Option 2: Using Make (if available)

From the backend directory:
```bash
make run  # Check Makefile for available commands
```

## Production Build

### Backend

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run build
npm start
```

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Linting

```bash
cd frontend
npm run lint
```

## Common Issues

### Backend won't start
- Check if port 8000 is already in use
- Verify DATABASE_URL is correctly set in `.env`
- Ensure virtual environment is activated

### Frontend won't start
- Check if port 3000 is already in use
- Verify `NEXT_PUBLIC_API_URL` is set in `.env.local`
- Try deleting `node_modules` and running `npm install` again

### CORS errors
- Ensure `PUBLIC_APP_URL` in backend `.env` matches your frontend URL
- Check that both servers are running

## API Endpoints

Main endpoints available at `http://localhost:8000`:

- `/api/orders` - Sales orders management
- `/api/production-orders` - Production order tracking
- `/api/deliveries` - Delivery management
- `/api/billings` - Billing and invoicing
- `/api/products` - Product catalog
- `/api/customers` - Customer management
- `/api/dashboard` - Dashboard analytics

Full API documentation: http://localhost:8000/docs

## Tech Stack

**Backend:**
- FastAPI
- SQLModel / SQLAlchemy
- PostgreSQL / SQLite
- Pydantic
- Uvicorn

**Frontend:**
- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- Zod
- Zustand
