import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime, timezone
import kivy
import time
import random
import threading
from kivy.app import App
from kivy.clock import Clock
from speedometer import Speedometer

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"

# InfluxDB Configuration
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "Vsx_ntOBe0LrzrbPaRvfNweulgDwOIaRDnuGOihkDPjfqCk12ThYHuT7rTXSQFGAsmhl4N4EW_eYNK5wTp4uQg=="
INFLUXDB_ORG = "Race Days"
INFLUXDB_BUCKET = "your_bucket"

# Initialize InfluxDB client
influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

class MyApp(App):
    def build(self):
        self.speedometer = Speedometer(size=(300, 300), pos=(100, 100))
        Clock.schedule_interval(self.update_speedometer, 1)  # Update every second
        return self.speedometer

    def update_speedometer(self, dt):
        # Fetch the latest data from InfluxDB
        query = f'from(bucket: "{INFLUXDB_BUCKET}") |> range(start: -1m) |> filter(fn: (r) => r._measurement == "{MQTT_TOPIC}") |> last()'
        result = influxdb_client.query_api().query(org=INFLUXDB_ORG, query=query)
        for table in result:
            for record in table.records:
                self.speedometer.value = record.get_value()

# MQTT Callback
def on_message(client, userdata, message):
    value = float(message.payload.decode('utf-8'))
    point = Point(MQTT_TOPIC).field("value", value).time(datetime.now(timezone.utc), WritePrecision.MS)
    influxdb_client.write_api(write_options=SYNCHRONOUS).write(bucket=INFLUXDB_BUCKET, record=point)
    
def generate_dummy_data():
    mqtt_clinet = mqtt.Client()
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    while True:
        mqtt_client.publish(MQTT_TOPIC, random.randint(0, 100))
        time.sleep(1)

# MQTT Client Setup
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()

dummy_data_thread = threading.Thread(target=generate_dummy_data)
dummy_data_thread.daemon = True
dummy_data_thread.start()

if __name__ == '__main__':
    MyApp().run()