import json
import paho.mqtt.client as mqtt
import tkinter as tk
from dataclasses import dataclass
from pymongo import MongoClient

from electronic_device_mqtt import ElectronicDevice

from solar_panel_mqtt import SolarPanel


def eval_policy_solar_panel(requesting_device: ElectronicDevice, solar_panel: SolarPanel, powered_devices):
    total_power = sum(device["work_power"] for device in powered_devices)
    return solar_panel.provided_power >= total_power + requesting_device.work_power

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
        requesting_device = ElectronicDevice(device_id=device_data["device_id"], work_power=device_data["work_power"])

        # Retrieve solar panel data from database
        solar_panel_data = self.collection.find_one({"device_id": "solar_panel"})

        # Retrieve all devices powered by solar panel
        powered_devices = self.collection.find({"powered_by": "solar_panel"})
        devices_list = list(powered_devices)
        # powered_devices = self.collection.find({"powered_by": "solar_panel"}, {"work_power": 1}) # Only work_power

        solar_panel = SolarPanel(device_id=solar_panel_data["device_id"],
                                 provided_power=solar_panel_data["provided_power"])

        # Evaluate policy
        result = eval_policy_solar_panel(requesting_device, solar_panel, devices_list)
        if result:
            print(f"The solar panel has enough power to power the {requesting_device}."
                  f" The {requesting_device} will be connected to the solar panel.")
            # Add a new field powered_by to the requesting_device document in the database
            self.collection.update_one({"device_id": device_data["device_id"]},
                                       {"$set": {"powered_by": solar_panel_data["device_id"]}})

        else:
            print(f"The solar panel does not have enough power to power the {requesting_device}. "
                  f"Do you want to unplug devices?")

            def on_select(device):
                nonlocal unused_power
                nonlocal color
                if device["selected"]:
                    # change button appearance when unselected
                    button.config(relief=tk.RAISED, bg="SystemButtonFace")

                    unused_power -= device["work_power"]
                else:
                    # change button appearance when selected
                    button.config(relief=tk.SUNKEN, bg="lightblue")

                    unused_power += device["work_power"]

                device["selected"] = not device["selected"]
                if unused_power >= requesting_device.work_power:
                    color = "green"
                else:
                    color = "red"
                unused_power_label.config(text=f"Unused power: {unused_power}", fg=color)

            def on_confirm():
                # Unplug all selected devices
                selected_devices = [device for device in devices_list if device["selected"]]
                for device in selected_devices:
                    self.collection.update_one({"device_id": device["device_id"]},
                                               {"$unset": {"powered_by": "solar_panel"}})
                # Evaluate policy again
                nonlocal result
                non_selected_devices = [device for device in devices_list if not device["selected"]]
                result = eval_policy_solar_panel(requesting_device, solar_panel, non_selected_devices)
                if result:
                    print(f"The solar panel has enough power to power the {requesting_device}."
                          f" The {requesting_device} will be connected to the solar panel.")
                    # Add a new field powered_by to the requesting_device document in the database
                    self.collection.update_one({"device_id": device_data["device_id"]},
                                               {"$set": {"powered_by": solar_panel_data["device_id"]}})
                else:
                    print(f"The solar panel does not have enough power to power the {requesting_device}. "
                          f"The {requesting_device} will not be connected to the solar panel.")

                root.destroy()

            root = tk.Tk()

            required_energy_label = tk.Label(root,
                                             text=f"Required Energy for the {requesting_device.device_id}:"
                                                  f" {requesting_device.work_power}")
            required_energy_label.pack()

            # Create a button for each device powered by the solar panel
            total_power = 0
            for device in devices_list:
                device_id = device["device_id"]
                work_power = device["work_power"]
                total_power += work_power
                device["selected"] = False
                button_text = f"{device_id}\n{work_power}"
                button = tk.Button(root, text=button_text, command=lambda d=device: on_select(d))
                button.pack()

            # Create a label for the provided power and unused power
            unused_power = solar_panel.provided_power - total_power
            power_frame = tk.Frame(root)
            provided_power_label = tk.Label(power_frame,
                                            text=f"Provided power by the solar panel: {solar_panel.provided_power}")
            provided_power_label.pack()
            if unused_power >= requesting_device.work_power:
                color = "green"
            else:
                color = "red"
            unused_power_label = tk.Label(power_frame, text=f"Unused power: {unused_power}", fg=color)
            unused_power_label.pack()
            power_frame.pack()

            # Create a confirm button to unplug selected devices
            confirm_button = tk.Button(root, text="Unplug selected devices.", command=on_confirm)
            confirm_button.pack()
            tk.mainloop()

        # Publish result to the requesting_device
        topic = f"policy_result/{requesting_device.device_id}"
        client.publish(topic, str(result))

    def clear_db(self):
        self.collection.delete_many({})
        print("Database cleared.")
