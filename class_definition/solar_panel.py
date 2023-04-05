from dataclasses import dataclass
from typing import List

from electronic_device import ElectronicDevice


@dataclass
class SolarPanel:
    provided_power: int
    powered_devices: List[ElectronicDevice]

    def plug_in(self, new_device: ElectronicDevice):
        self.provided_power -= new_device.work_power
        self.powered_devices.append(new_device)

    def plug_out(self, old_device: ElectronicDevice):
        try:
            self.powered_devices.remove(old_device)
            self.provided_power += old_device.work_power
        except ValueError:
            return f"Device is not plugged in."

    def get_rated_power(self):
        return self.provided_power

    def get_powered_devices(self):
        json_output = []
        for device in self.powered_devices:
            json_output.append(device.get_json_work_power())
        return json_output

