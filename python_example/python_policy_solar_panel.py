from electronic_device import ElectronicDevice
from solar_panel import SolarPanel


def eval_policy_solar_panel(requesting_device: ElectronicDevice, solar_panel: SolarPanel, powered_devices):
    return solar_panel.provided_power >= sum(device.work_power for device in powered_devices) + requesting_device.work_power
