import yaml
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
import time
import random

# Load credentials from YAML file
with open("credentials.yaml", 'r') as stream:
    try:
        credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Initialize InfluxDB client
influxdb_client = InfluxDBClient(url=credentials['influxdb']['url'], 
                                 token=credentials['influxdb']['token'], 
                                 org=credentials['influxdb']['org']
                                 )

# Topics to generate dummy data for
topics = ["herzfrequenz", "leistung", "geschwindigkeit"]

while True: #infinite loop to generate data

    for topic in topics:
        # Generate a random integer between 25 and 100
        value = random.randint(25, 100)

        # Create a new point and write it to InfluxDB
        with influxdb_client.write_api(write_options=SYNCHRONOUS) as write_api:
            p = Point(topic) \
                .field("value", value) \
                .time(datetime.now(timezone.utc), WritePrecision.MS)
            write_api.write(bucket='tests', record=p)

        # Wait for 1 second before generating the next set of data
        time.sleep(3)
    