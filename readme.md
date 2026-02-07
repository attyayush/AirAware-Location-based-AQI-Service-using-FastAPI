# AirAware: Location-based AQI Service


##  Design Decisions

As per the project requirements, the following architectural choices were made:

### 1. Selection of ipwho.is and Open-Meteo
These specific APIs were selected for two primary reasons:
* **Ease of Integration**: Both services offer high-quality data without requiring complex API keys or registration, which simplifies the deployment and testing process for reviewers.
* **Reliability & Accuracy**: `ipwho.is` provides comprehensive JSON responses including coordinates, while `Open-Meteo` is a gold standard for open-access meteorological data, providing high-resolution AQI updates.

### 2. Caching Strategy
To optimize performance and reduce redundant external API calls, the system is designed to implement an **In-Memory TTL (Time-To-Live) Cache** (e.g., using `cachetools`).
* **TTL**: 15 minutes.
* **Logic**: Since air quality and location data do not change every second, caching results for 15 minutes significantly reduces latency for repeat users and prevents hitting rate limits on the external providers.

### 3. Handling of Private/Local IP Addresses
A common issue in development is the client IP appearing as `127.0.0.1` (localhost) or a private network range (e.g., `192.168.x.x`).
* **Solution**: The system includes a fallback mechanism. If the detected IP is a local/private address, the service uses `ipify` to fetch the server's public outbound IP. This ensures the geolocation service always receives a valid, routable IP address to resolve.
## Features
- ## Automatic IP Detection: Uses `ipify` to detect public IP.
- ## Geolocation: Resolves IP to City/Region/Coordinates via `ipwho.is`.
- ## Real-time AQI: Fetches data from Open-Meteo Air Quality API.
- ## Async Architecture: Non-blocking requests using `httpx`.

## Tech Stack
- FastAPI, Uvicorn, Pydantic, HTTPX, Loguru.
- - **Frontend**: HTML5, CSS3, JavaScript (Fetch API)
- - **Caching**: Cachetools (TTL Cache)

## How to Run
1. Clone the repository.
2. Install dependencies:
   ```bash

   pip install -r requirements.txt
3. Backend Start: python -m uvicorn main:app --reload
   4.Look for the message INFO: Application startup complete.
4. Open browser and go to: http://127.0.0.1:8000/health

 You should see: {"status": "ok"}. By writing down any city name after  http://127.0.0.1:8000/aqi/by-city?name- you will get AQI of that city and http://127.0.0.1:8000/aqi gives AQI of current location.
 
 5.Run index.html
 
 6.At database in MongoDB,open the aqi_history collection. You should see a new "Document" with your IP, City, and the AQI value you just fetched.



