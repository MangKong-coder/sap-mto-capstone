from fastapi import FastAPI
from app.api import api_router
from app.core.config import settings

app = FastAPI(title="MTO Backend", version="0.1.0")
app.include_router(api_router, prefix="/api/v1")

# @app.get("/config")
# def read_config():
#     return {"debug": settings.debug, "db_url": settings.database_url}

@app.get("/")
def root():
    return {"ok": True, "service": "mto-backend"}


