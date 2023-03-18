from dataclasses import dataclass
from typing import List


@dataclass
class ElectronicDevice:
    work_power: int


@dataclass
class SmartPlug:
    rated_power: int
    plugged_devices: List[ElectronicDevice]
    slots: int

    def plug_in(self, new_device: ElectronicDevice):
        self.rated_power -= new_device.work_power
        self.plugged_devices.append(new_device)
        self.slots -= 1

    def plug_out(self, old_device: ElectronicDevice):
        try:
            self.plugged_devices.remove(old_device)
            self.rated_power += old_device.work_power
            self.slots += 1
        except ValueError:
            return f"Device is not plugged in."

