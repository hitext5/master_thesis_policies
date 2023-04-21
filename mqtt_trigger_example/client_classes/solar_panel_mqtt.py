import json
import paho.mqtt.client as mqtt
from dataclasses import dataclass
from typing import List

from electronic_device_mqtt import ElectronicDevice
from python_example.python_policy_solar_panel import eval_policy_solar_panel


@dataclass
class SolarPanel:
    mqtt_id: str
    provided_power: int
    powered_devices: List[ElectronicDevice]
    broker = "127.0.0.1"
    port = 1883
    rc = 1

    def __post_init__(self):
        self.client = mqtt.Client(client_id=self.mqtt_id)

    def on_connect(self, client, userdata, flags, rc):
        self.rc = rc
        if rc == 0:
            print("SolarPanel connected to MQTT Broker!")
            client.subscribe("device/+/on")
            # client.subscribe("device/+/off")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        device_data = json.loads(msg.payload)
        device = ElectronicDevice(mqtt_id=device_data["device_id"], work_power=device_data["work_power"])
        # TODO I need to subscribe to multiple topics to trigger different policies
        #  or use state pattern in the ElectronicDevice class.
        # if msg.topic.endswith("/on"):
        #     result = eval_policy_solar_panel(device, self)
        # elif msg.topic.endswith("/off"):
        #     result = eval_policy_two(device, self)
        # else:
        #     result = "Unknown topic"
        result = eval_policy_solar_panel(device, self)
        topic = f"solar_panel/policy_result/{device.mqtt_id}"
        client.publish(topic, str(result))

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)
        # Send message to server to store the device in the database.
