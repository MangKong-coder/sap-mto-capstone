from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.api.main import api_router
import uvicorn

app = FastAPI(
    title="CORES-CAPSTONE-BACKEND",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to CORES-CAPSTONE-BACKEND!"}

app.include_router(api_router, prefix='/v1')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
