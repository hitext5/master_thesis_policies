from electronic_device import ElectronicDevice
from solar_panel import SolarPanel


def eval_policy_solar_panel(requesting_device: ElectronicDevice, solar_panel: SolarPanel):
    total_power = sum(device.work_power for device in solar_panel.powered_devices)
    return solar_panel.provided_power >= total_power + requesting_device.work_power
