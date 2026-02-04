from pydantic import BaseModel

class LocationSchema(BaseModel):
    city: str
    region: str
    country: str
    lat: float
    lon: float

class AQISchema(BaseModel):
    value: int
    category: str

class AirQualityResponse (BaseModel):
    ip: str
    location: LocationSchema
    aqi: AQISchema
    source: str = "open-meteo"
