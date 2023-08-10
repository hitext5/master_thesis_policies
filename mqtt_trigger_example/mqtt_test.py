import time

from electronic_device_mqtt import ElectronicDevice
from message_handler_mqtt import MessageHandler
from solar_panel_mqtt import SolarPanel

# C:\Program Files\mosquitto
# mosquitto -v
# If the port is already listening
# netstat -ano | findstr :1883
# taskkill /pid 7392 /F
# Run mosquitto -v in a terminal to see the messages being sent and received.
message_handler = MessageHandler()
washing_machine = ElectronicDevice(device_id="washing_machine", work_power=400)
washer = ElectronicDevice(device_id="washer", work_power=200)
solar_panel = SolarPanel(device_id="solar_panel", provided_power=500)

message_handler.connect()
message_handler.client.loop_start()
print("MessageHandler loop started")
while message_handler.rc != 0:
    time.sleep(1)

washing_machine.connect()
washing_machine.client.loop_start()
print("Washer loop started")
while washing_machine.rc != 0:
    time.sleep(1)
# time.sleep(15)

washer.connect()
washer.client.loop_start()
print("Washing machine loop started")
while washer.rc != 0:
    time.sleep(1)
# time.sleep(15)

solar_panel.connect()
solar_panel.client.loop_start()
print("Solar panel loop started")
while solar_panel.rc != 0:
    time.sleep(1)
# time.sleep(15)

washing_machine.turn_on()
# message_handler.clear_db()
