import casbin

from electronic_device import ElectronicDevice
from solar_panel import SolarPanel


def test_solar_panel():
    # Initialize the Casbin object.
    e = casbin.Enforcer("casbin_model.conf", "casbin_policy.csv")

    hairdryer = ElectronicDevice(work_power=40)
    fan = ElectronicDevice(work_power=30)
    charger = ElectronicDevice(work_power=30)
    solar_panel = SolarPanel(provided_power=110, powered_devices=[hairdryer, fan])

    assert e.enforce(charger, solar_panel)
