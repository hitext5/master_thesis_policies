import time

from electronic_device_mqtt import ElectronicDevice
from message_handler_mqtt import MessageHandler
from solar_panel_mqtt import SolarPanel

# C:\Program Files\mosquitto
# mosquitto -v
# Run mosquitto -v in a terminal to see the messages being sent and received.

message_handler = MessageHandler()
washer = ElectronicDevice(device_id="washer", work_power=400)
washing_machine = ElectronicDevice(device_id="washing_machine", work_power=200)
solar_panel = SolarPanel(device_id="solar_panel", provided_power=600)

message_handler.connect()
message_handler.client.loop_start()
print("MessageHandler loop started")
while message_handler.rc != 0:
    time.sleep(1)

washer.connect()
washer.client.loop_start()
print("Washer loop started")
while washer.rc != 0:
    time.sleep(1)
time.sleep(15)

washing_machine.connect()
washing_machine.client.loop_start()
print("Washing machine loop started")
while washing_machine.rc != 0:
    time.sleep(1)
time.sleep(15)

solar_panel.connect()
solar_panel.client.loop_start()
print("Solar panel loop started")
while solar_panel.rc != 0:
    time.sleep(1)
time.sleep(15)

washing_machine.turn_on()
time.sleep(15)
message_handler.clear_db()
time.sleep(60)
