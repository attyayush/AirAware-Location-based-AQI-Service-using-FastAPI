import httpx
from loguru import logger

async def get_client_ip():
    url = "https://api.ipify.org?format=json"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            response.raise_for_status() # Check if the request actually worked
            return response.json().get("ip")
        except Exception as e:
            logger.error(f"Error fetching IP: {e}")
            return None
