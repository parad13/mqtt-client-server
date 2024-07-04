# client.py
import paho.mqtt.client as mqtt
import time
import random
import json

# MQTT broker settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/status"

# Callback for when the client receives a connect response from the server.
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")

# Callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.payload)}")

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the loop in a non-blocking way
client.loop_start()

# Main loop
try:
    while True:
        # Generate random status
        status = random.randint(0, 6)
        
        # Create message payload
        payload = {
            "status": status,
            "timestamp": int(time.time())
        }
        
        # Publish message
        client.publish(MQTT_TOPIC, json.dumps(payload))
        
        # Wait for 1 second
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Stopping client...")
finally:
    client.loop_stop()
    client.disconnect()
    print("Client stopped.")