import httpx

def interpret_aqi(value):
    if value <= 50: return "Good"
    if value <= 100: return "Moderate"
    if value <= 150: return "Unhealthy for Sensitive Groups"
    if value <= 200: return "Unhealthy"
    return "Very Unhealthy"

async def get_air_quality(lat: float, lon: float):
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        aqi_val = data["current"]["us_aqi"]
        return {"value": aqi_val, "category": interpret_aqi(aqi_val)}
