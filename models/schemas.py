from pydantic import BaseModel
from typing import Optional

class LocationInfo(BaseModel):
    city: str
    region: str
    country: str
    lat: float
    lon: float

class AQIInfo(BaseModel):
    value: int
    category: str

class AirQualityResponse(BaseModel):
    ip: Optional[str] = "N/A"
    location: LocationInfo
    aqi: AQIInfo
    source: str = "open-meteo"
