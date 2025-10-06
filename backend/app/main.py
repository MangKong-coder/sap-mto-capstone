from fastapi import FastAPI
from app.database import init_db
from . import models
from app.api import orders
# from app.routers import orders, production, deliveries, billing

app = FastAPI(title="Mapúa MTO Backend")

@app.on_event("startup")
def on_startup():
    init_db()

# Include routers
app.include_router(orders.router)
# app.include_router(production.router)
# app.include_router(deliveries.router)
# app.include_router(billing.router)
