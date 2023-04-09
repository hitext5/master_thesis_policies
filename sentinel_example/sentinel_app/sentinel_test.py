import json
import subprocess

from electronic_device import ElectronicDevice
from solar_panel import SolarPanel


def test_solar_panel():
    # Define a function to update the plug_json
    def apply_policy(requesting_device: ElectronicDevice, providing_solar_panel: SolarPanel):
        try:
            # Update the json files
            with open('electronic_device.json', 'w') as f:
                json.dump({"work_power": requesting_device.work_power}, f)

            with open('solar_panel.json', 'w') as f:
                json.dump({"provided_power": providing_solar_panel.get_provided_power(),
                           "powered_devices": solar_panel.get_powered_devices()}, f)

            # Run the policy
            output = subprocess.check_output("sentinel apply sentinel_policy_solar_panel.sentinel")
            output_str = output.decode("utf-8")
            if "Pass" in output_str:
                return True
            else:
                return False
        except subprocess.CalledProcessError:
            return False

    hairdryer = ElectronicDevice(work_power=40)
    fan = ElectronicDevice(work_power=30)
    charger = ElectronicDevice(work_power=30)
    solar_panel = SolarPanel(provided_power=110, powered_devices=[hairdryer, fan])

    assert apply_policy(charger, solar_panel)
