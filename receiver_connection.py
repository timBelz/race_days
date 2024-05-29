import yaml
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone

# Load credentials from YAML file
with open("credentials.yaml", 'r') as stream:
    try:
        credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# MQTT Broker Configuration
broker_address = credentials['mqtt']['broker_address']
port = credentials['mqtt']['port']

# Initialize InfluxDB client
influxdb_client = InfluxDBClient(url=credentials['influxdb']['url'], 
                                 token=credentials['influxdb']['token'], 
                                 org=credentials['influxdb']['org']
                                 )

# Callback function for each sensor data type
def on_message(client, userdata, message):
    
    # Create a new point and write it to InfluxDB
    with influxdb_client.write_api(write_options=SYNCHRONOUS) as write_api:
        p = Point(message.topic) \
            .field("value", int(message.payload.decode('utf-8'))) \
            .time(datetime.now(timezone.utc), WritePrecision.MS)
        write_api.write(bucket='sensor_viz', record=p)

# MQTT Client initialisieren und Callbacks festlegen
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_message = on_message

client.connect(broker_address, port)

# Subscribe to topics
client.subscribe("herzfrequenz")
client.subscribe("leistung")
client.subscribe("geschwindigkeit")

# Start MQTT client
client.loop_forever()