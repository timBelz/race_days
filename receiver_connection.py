import paho.mqtt.client as mqtt


TOPIC = "Herzfrequenz"
BROKER_ADRESS = "localhost"
PORT = 1883
QOS = 1

class mqttSend(object):
    def __init__(self):
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.connect(BROKER_ADRESS, PORT)
        self.observer = None
        
        print("Connect to MQTT Broker: " + BROKER_ADRESS)
        data = "{TEST_DATA}"
        
        client.publish(TOPIC, data, QOS)
        client.loop()

        
    def __del__(self):
        print("Nothing to delete. Existing.")
        
    def update(self, payload):
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.connect(BROKER_ADRESS, PORT)
        client.publish(TOPIC, payload, QOS)
        client.loop()
        return payload