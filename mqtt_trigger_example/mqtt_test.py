import time

from electronic_device_mqtt import ElectronicDevice
from solar_panel_mqtt import SolarPanel

# mosquitto -v
# Run mosquitto -v in a terminal to see the messages being sent and received.

washer = ElectronicDevice(mqtt_id="washer", work_power=400)
washing_machine = ElectronicDevice(mqtt_id="washing_machine", work_power=200)
solar_panel = SolarPanel(mqtt_id="solar_panel", provided_power=600, powered_devices=[washer])

washer.connect()
washer.client.loop_start()
print("Washer loop started")
while washer.rc != 0:
    time.sleep(1)
washing_machine.connect()
washing_machine.client.loop_start()
print("Washing machine loop started")
while washing_machine.rc != 0:
    time.sleep(1)
solar_panel.connect()
solar_panel.client.loop_start()
print("Solar panel loop started")
while solar_panel.rc != 0:
    time.sleep(1)

washing_machine.turn_on()
time.sleep(5)
