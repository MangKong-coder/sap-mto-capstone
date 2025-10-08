from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.database import init_db
from . import models
from app.api import orders, production_orders, deliveries, billings, products, customers, dashboard
from fastapi.middleware.cors import CORSMiddleware
import os

from dotenv import load_dotenv  


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    load_dotenv()

    init_db()
    yield
    # Shutdown (if needed)


app = FastAPI(title="Mapúa MTO Backend", lifespan=lifespan)

load_dotenv()
APP_URL = os.environ.get("PUBLIC_APP_URL")

origins = [
    APP_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders.router)
app.include_router(production_orders.router)
app.include_router(deliveries.router)
app.include_router(billings.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(dashboard.router)
