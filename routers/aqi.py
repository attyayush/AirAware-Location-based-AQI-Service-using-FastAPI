from fastapi import APIRouter, HTTPException, Request
from models.schemas import AirQualityResponse
from services.ip_service import get_client_ip
from services.geo_service import get_location_data
from services.aqi_service import get_air_quality
from loguru import logger

router = APIRouter()

@router.get("/aqi", response_model=AirQualityResponse)
async def get_current_location_aqi(request: Request):
    logger.info("Received request for current location AQI")

    
    client_ip = request.client.host
    if client_ip in ("127.0.0.1", "localhost"):
        client_ip = await get_client_ip()

    if not client_ip:
        raise HTTPException(status_code=500, detail="Could not detect client IP")

    
    geo_data = await get_location_data(client_ip)
    if not geo_data:
        raise HTTPException(status_code=404, detail="Location data not found")

    
    aqi_data = await get_air_quality(geo_data["lat"], geo_data["lon"])
    if not aqi_data:
        raise HTTPException(status_code=500, detail="AQI data retrieval failed")

  
    return AirQualityResponse(
        ip=client_ip,
        location=geo_data,
        aqi=aqi_data
    )