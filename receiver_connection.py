import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone

# MQTT Broker Configuration
broker_address = "192.168.178.202"
port = 1883

# InfluxDB Configuration
url = 'http://localhost:8086/orgs/08762263b5ca87d3'
token = '352VYvG1n5N17ayto3Fqc2ixcoDBdxhmPTt3WyHvn1eg1QJ6e1Ha0QkWEEAJ5JQL3VnbxrBjVLRpAdWXz6xCAA=='
org = 'Race Days'
bucket = 'sensor_viz'

# Initialize InfluxDB client
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

# Callback function for each sensor data type
def on_message(client, userdata, message):
    # Create a new point and write it to InfluxDB
    with influxdb_client.write_api(write_options=SYNCHRONOUS) as write_api:
        p = Point(message.topic) \
            .field("value", float(message.payload.decode('utf-8'))) \
            .time(datetime.now(timezone.utc), WritePrecision.MS)
        write_api.write(bucket=bucket, record=p)

# Initialize MQTT client and set callbacks
client = mqtt.Client()

client.on_message = on_message

client.connect(broker_address, port)

# Subscribe to topics
client.subscribe("herzfrequenz")
client.subscribe("leistung")

# Start MQTT client
client.loop_forever()