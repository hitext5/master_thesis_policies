import json
import paho.mqtt.client as mqtt
from dataclasses import dataclass


@dataclass
class ElectronicDevice:
    mqtt_id: str
    work_power: int
    broker = "127.0.0.1"
    port = 1883
    rc = 1

    def __post_init__(self):
        self.client = mqtt.Client(client_id=self.mqtt_id)

    def on_connect(self, client, userdata, flags, rc):
        self.rc = rc
        if rc == 0:
            print(f"{self.mqtt_id.capitalize()} connected to MQTT Broker!")
            topic = f"solar_panel/policy_result/{self.mqtt_id}"
            client.subscribe(topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        if msg.payload.decode():
            print("The solar panel has enough power to power the washing machine.")
        else:
            print("The solar panel does not have enough power to power the washing machine.")

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)
        # Send message to server to store the device in the database.

    def turn_on(self):
        topic = f"device/{self.mqtt_id}/on"
        payload = {"device_id": self.mqtt_id, "work_power": self.work_power}
        self.client.publish(topic, json.dumps(payload))
