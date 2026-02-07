import httpx


async def get_location_data(ip: str):
    url = f"https://ipwho.is/{ip}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if not data.get("success"): return None
        return {
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "lat": data.get("latitude"),
            "lon": data.get("longitude")
        }

async def get_coords_by_city(city_name: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if not data.get("results"): return None
        res = data["results"][0]
        return {
            "city": res["name"],
            "region": res.get("admin1", "N/A"),
            "country": res["country"],
            "lat": res["latitude"],
            "lon": res["longitude"]
        }
