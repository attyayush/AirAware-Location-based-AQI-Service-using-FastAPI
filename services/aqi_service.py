import httpx
from loguru import logger

def get_aqi_category(aqi_value: int) -> str:
    """Standard US EPA AQI Categories"""
    if aqi_value <= 50: return "Good"
    elif aqi_value <= 100: return "Moderate"
    elif aqi_value <= 150: return "Unhealthy for Sensitive Groups"
    elif aqi_value <= 200: return "Unhealthy"
    elif aqi_value <= 300: return "Very Unhealthy"
    return "Hazardous"

async def get_air_quality(lat: float, lon: float):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "us_aqi"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            
            aqi_val = data["current"]["us_aqi"]
            return {
                "value": int(aqi_val),
                "category": get_aqi_category(aqi_val)
            }
        except Exception as e:
            logger.error(f"AQI service error: {e}")
            return None
