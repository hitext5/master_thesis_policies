import json
import paho.mqtt.client as mqtt
from dataclasses import dataclass
from pymongo import MongoClient

from electronic_device_mqtt import ElectronicDevice
from python_example.python_policy_solar_panel import eval_policy_solar_panel
from solar_panel_mqtt import SolarPanel


@dataclass
class MessageHandler:
    device_id = "message_handler"
    broker: str = "127.0.0.1"
    port: int = 1883
    client = mqtt.Client(client_id=device_id)
    rc = 1
    atlas_uri = "mongodb://Kleriakanus:test123@ac-s2miieu-shard-00-00.s0mnged.mongodb.net:27017," \
                "ac-s2miieu-shard-00-01.s0mnged.mongodb.net:27017," \
                "ac-s2miieu-shard-00-02.s0mnged.mongodb.net:27017/?ssl=true&replicaSet=atlas-vihgip-shard-0" \
                "&authSource=admin&retryWrites=true&w=majority"
    db_name = 'Cluster0'
    mongo_client = MongoClient(atlas_uri)
    database = mongo_client[db_name]
    collection = database["devices"]

    def on_connect(self, client, userdata, flags, rc):
        self.rc = rc
        if rc == 0:
            print("MessageHandler connected to MQTT Broker!")
            # Basic MQTT topics (we assume that all devices publish to these topics)
            client.subscribe("device/+/connected")
            # Specify the callback function for the subscribed topics
            client.message_callback_add("device/+/connected", self.connection_message)
            client.subscribe("device/+/disconnected")
            client.message_callback_add("device/+/disconnected", self.disconnection_message)
            client.subscribe("check_policy/+")
            client.message_callback_add("check_policy/+", self.check_policy_message)
        else:
            print("Failed to connect, return code %d\n", rc)
        pass

    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def connection_message(self, client, userdata, msg):
        device_data = json.loads(msg.payload)
        print(f"{device_data} connected to the system.")
        # Save device data to database on first connection
        self.collection.insert_one(device_data)

    def disconnection_message(self, client, userdata, msg):
        device_data = json.loads(msg.payload)
        print("Device disconnected from the system.")
        # Delete device data from database on disconnection
        self.collection.delete_one({"mqtt_id": device_data["device_id"]})

    def check_policy_message(self, client, userdata, msg):
        # TODO Currently specific to solar panel policy
        device_data = json.loads(msg.payload)
        device = ElectronicDevice(device_id=device_data["device_id"], work_power=device_data["work_power"])

        # Retrieve solar panel data from database
        solar_panel_data = self.collection.find_one({"device_id": "solar_panel"})

        # Retrieve all devices powered by solar panel
        powered_devices = self.collection.find({"powered_by": "solar_panel"})
        # powered_devices = self.collection.find({"powered_by": "solar_panel"}, {"work_power": 1}) # Only work_power

        solar_panel = SolarPanel(device_id=solar_panel_data["device_id"],
                                 provided_power=solar_panel_data["provided_power"])

        # Evaluate policy
        result = eval_policy_solar_panel(device, solar_panel, powered_devices)
        if result:
            # Update database
            print(f"The solar panel has enough power to power the {device}.")
            self.collection.update_one({"device_id": device_data["device_id"]},
                                       {"$set": {"powered_by": solar_panel_data["device_id"]}})

            # TODO Show notification on the UI
        else:
            print(f"The solar panel does not have enough power to power the {device}.")
            # Show notification on the UI

        # Publish result to the device
        topic = f"policy_result/{device.device_id}"
        client.publish(topic, str(result))

    def clear_db(self):
        self.collection.delete_many({})
        print("Database cleared.")
