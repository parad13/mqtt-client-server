# server.py
import paho.mqtt.client as mqtt
import pika
import json
import time
from pymongo import MongoClient
from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# MongoDB settings
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "status_messages"

# MQTT settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/status"

# RabbitMQ settings
RABBITMQ_HOST = "localhost"

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)


# MQTT on_message callback
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    
    # Store message in MongoDB
    collection.insert_one(payload)

# Set up MQTT client
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start MQTT loop in a separate thread
mqtt_client.loop_start()

# Set up RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='mqtt_queue')

# Pydantic model for response
class StatusCounts(BaseModel):
    counts: dict[int, int]

# Endpoint to get status counts
@app.get("/status_counts", response_model=StatusCounts)
async def get_status_counts(
    start_time: Optional[int] = Query(None, description="Start timestamp"),
    end_time: Optional[int] = Query(None, description="End timestamp")
):
    start_time = start_time or 0
    end_time = end_time or int(time.time())
    
    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start_time, "$lte": end_time}
            }
        },
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]
    
    result = list(collection.aggregate(pipeline))
    
    # Convert result to a more readable format
    status_counts = {item["_id"]: item["count"] for item in result}
    
    return StatusCounts(counts=status_counts)

if __name__ == '__main__':
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("Stopping MQTT client...")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("MQTT client stopped.")