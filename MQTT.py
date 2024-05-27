import paho.mqtt.client as mqtt

# MQTT Broker Konfiguration
broker_address = "192.168.178.202"
port = 1883

# Callback-Funktionen für jede Sensordatenart

def on_message(client, userdata, message):
	heartbeat = f"'{message.topic}': {message.payload.decode('utf-8')}"
	return heartbeat

# print(f"Userdata: '{userdata}'")

# MQTT Client initialisieren und Callbacks festlegen
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_message = on_message

client.connect(broker_address, port)

# Alle Themen und Unterthemen abonnieren
# client.subscribe("#")
# Nur Herzfrequenz abonnieren
client.subscribe("herzfrequenz")
client.subscribe("leistung")


# MQTT Client starten
client.loop_forever()