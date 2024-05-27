from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone

# Connect to InfluxDB
client = InfluxDBClient(url="http://localhost:8086", 
                        token="352VYvG1n5N17ayto3Fqc2ixcoDBdxhmPTt3WyHvn1eg1QJ6e1Ha0QkWEEAJ5JQL3VnbxrBjVLRpAdWXz6xCAA==", 
                        org="Race Days"
                        )

# Get the write API
write_api = client.write_api(write_options=SYNCHRONOUS)

# Write a point to the 'test' bucket
point = Point("my_measurement").field("value", 400.00).time(datetime.now(timezone.utc), WritePrecision.NS)
write_api.write("sensor_viz", "Race Days", point)