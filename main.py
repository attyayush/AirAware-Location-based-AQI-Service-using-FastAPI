from fastapi import FastAPI
from routers import aqi

app = FastAPI(title="AirAware API")


app.include_router(aqi.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)