import httpx
from loguru import logger

async def get_location_data(ip_address: str):
    if not ip_address:
        return None
        
    url = f"https://ipwho.is/{ip_address}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            data = response.json()
            
            if not data.get("success"):
                logger.warning(f"Geo lookup failed for IP: {ip_address}")
                return None
            
            return {
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
                "lat": data.get("latitude"),
                "lon": data.get("longitude")
            }
        except Exception as e:
            logger.error(f"Geo service error: {e}")
            return None