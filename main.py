from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import aqi

app = FastAPI(title="AirAware API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aqi.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
