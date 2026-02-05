import httpx
from loguru import logger
from cachetools import TTLCache 


aqi_cache = TTLCache(maxsize=100, ttl=900)

def get_aqi_category(aqi_value: int) -> str:
    """Standard US EPA AQI Categories"""
    if aqi_value <= 50: return "Good"
    elif aqi_value <= 100: return "Moderate"
    elif aqi_value <= 150: return "Unhealthy for Sensitive Groups"
    elif aqi_value <= 200: return "Unhealthy"
    elif aqi_value <= 300: return "Very Unhealthy"
    return "Hazardous"

async def get_air_quality(lat: float, lon: float):
   
    cache_key = f"{lat}_{lon}"
    if cache_key in aqi_cache:
        logger.info(f"Returning CACHED AQI for {lat}, {lon}")
        return aqi_cache[cache_key]

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "us_aqi"
    }
    
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            logger.info(f"Fetching fresh AQI from Open-Meteo for {lat}, {lon}")
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            aqi_val = data["current"]["us_aqi"]
            result = {
                "value": int(aqi_val),
                "category": get_aqi_category(aqi_val)
            }

            
            aqi_cache[cache_key] = result
            return result

        except httpx.TimeoutException:
            logger.error("AQI service timed out")
            return None
        except Exception as e:
            logger.error(f"AQI service error: {e}")
            return None
            
   
