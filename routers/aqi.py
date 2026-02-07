from fastapi import APIRouter, HTTPException, Request
from models.schemas import AirQualityResponse
from models.database import log_aqi_request, get_total_request_count, get_recent_history
from services.ip_service import get_client_ip
from services.geo_service import get_location_data
from services.aqi_service import get_air_quality
from datetime import datetime
from services.geo_service import get_location_data, get_coords_by_city

router = APIRouter()

@router.get("/aqi", response_model=AirQualityResponse)
async def get_current_location_aqi(request: Request):
    
    client_ip = await get_client_ip()
    geo_data = await get_location_data(client_ip)
    if not geo_data:
        raise HTTPException(status_code=404, detail="Location not found")
        
    aqi_data = await get_air_quality(geo_data["lat"], geo_data["lon"])
    
    
    result = {
        "ip": client_ip,
        "location": geo_data,
        "aqi": aqi_data,
        "source": "open-meteo",
        "timestamp": datetime.utcnow()
    }
    
   
    await log_aqi_request(result)
    return result

@router.get("/aqi/stats")
async def get_stats():
    count = await get_total_request_count()
    return {"total_requests": count}

@router.get("/aqi/history")
async def get_history():
    return await get_recent_history(10)
@router.get("/aqi/by-city", response_model=AirQualityResponse)
async def get_aqi_by_city(name: str):
    
    geo_data = await get_coords_by_city(name)
    if not geo_data:
        raise HTTPException(status_code=404, detail=f"City '{name}' not found")
    
   
    aqi_data = await get_air_quality(geo_data["lat"], geo_data["lon"])
    
  
    result = {
        "ip": "City-Search",
        "location": geo_data,
        "aqi": aqi_data,
        "source": "open-meteo",
        "timestamp": datetime.utcnow()
    }
    
    await log_aqi_request(result)
    
    return result
