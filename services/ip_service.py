import httpx

async def get_client_ip():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.ipify.org?format=json", timeout=5.0)
            return response.json().get("ip")
        except Exception:
            return "127.0.0.1"
