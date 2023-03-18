import casbin

from electronic_device import ElectronicDevice
from smart_plug import SmartPlug


# Check if the device is allowed to plug into the smart plug
def test_basic_casbin():
    # Initialize the Casbin object.
    e = casbin.Enforcer("model.conf", "policy.csv")

    # Create an instance of ElectronicDevice with a work_power of 40
    hairdryer = ElectronicDevice(work_power=40)

    # Create an instance of ElectronicDevice with a work_power of 30
    fan = ElectronicDevice(work_power=30)

    # Create an instance of ElectronicDevice with a work_power of 30
    charger = ElectronicDevice(work_power=30)

    # Create an instance of SmartPlug with a rated_power of 90 and an empty list for plugged_devices
    plug = SmartPlug(rated_power=90, plugged_devices=[], slots=5)

    assert e.enforce(hairdryer, plug, "plug_in")
    plug.plug_in(hairdryer)

    assert e.enforce(fan, plug, "plug_in")
    plug.plug_in(fan)

    assert not e.enforce(charger, plug, "plug_in")
    plug.plug_in(charger)
