from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

MONGO_URL = "mongodb+srv://AYUSH:123@cluster0.cz6udsg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = AsyncIOMotorClient(MONGO_URL)
database = client.airaware_db
aqi_collection = database.get_collection("aqi_logs")

async def log_aqi_request(data: dict):
    """Saves the AQI response to MongoDB"""
    try:
        
        if "timestamp" not in data:
            data["timestamp"] = datetime.utcnow()
        await aqi_collection.insert_one(data)
    except Exception as e:
        print(f"MongoDB Log Error: {e}")

async def get_total_request_count():
    """Returns total number of records"""
    return await aqi_collection.count_documents({})

async def get_recent_history(limit=5):
    """Returns the last few records, newest first"""
    cursor = aqi_collection.find().sort("timestamp", -1).limit(limit)
    history = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"]) 
        history.append(doc)
    return history