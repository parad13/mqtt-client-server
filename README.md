# MQTT Client-Server with RabbitMQ and MongoDB

This project demonstrates a client-server architecture for handling MQTT messages using RabbitMQ as the MQTT broker and MongoDB for storing the data. The client script simulates an IoT device by publishing random status values as MQTT messages every second. The server script processes these messages, stores them in MongoDB, and provides an API endpoint to retrieve status counts within a specified time range.

## Features

- MQTT messaging integration with RabbitMQ
- Client script for publishing simulated IoT data
- Server script for processing MQTT messages and storing data in MongoDB
- FastAPI endpoint for retrieving status counts based on a time range
- MongoDB aggregation pipeline for efficient data querying

## Prerequisites

- Python 3.6 or higher
- MongoDB
- RabbitMQ
- MQTT broker (Mosquitto)

## Installation

1. Clone the repository: git clone https://github.com/parad13/mqtt-client-server.git

2. Navigate to the project directory:
   cd mqtt-client-server

3. Install the required Python packages:
   pip install -r requirements.txt

## Usage

1. Start the MongoDB, RabbitMQ, and MQTT broker services.

2. Run the server script:
   python server.py

3. In a separate terminal, run the client script:
   python client.py

4. To retrieve status counts, send a GET request to the `/status_counts` endpoint with the `start_time` and `end_time` query parameters: http://localhost:8000/status_counts?start_time=1625097600&end_time=1625184000

This will return a JSON object with the count of each status within the specified time range.

## Configuration

You can modify the following settings in the `server.py` and `client.py` files:

- MongoDB connection URI
- RabbitMQ host
- MQTT broker host and port
- MQTT topic


