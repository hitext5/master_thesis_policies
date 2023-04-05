import casbin

from electronic_device import ElectronicDevice
from solar_panel import SolarPanel


# def overall_power(objects: list[ElectronicDevice], subject: SmartPlug):
#     overall = 0
#     for obj in objects:
#         overall += obj.work_power
#     if subject.rated_power >= overall:
#         return True
#     else:
#         return False
#


# Check if the device is allowed to plug into the smart plug
def test_basic_casbin():
    # Initialize the Casbin object.
    e = casbin.Enforcer("casbin_model.conf", "casbin_policy.csv")

    # e.add_function("test", overall_power)

    # Create an instance of ElectronicDevice with a work_power of 40
    hairdryer = ElectronicDevice(work_power=100)

    # Create an instance of ElectronicDevice with a work_power of 30
    fan = ElectronicDevice(work_power=50)

    # Create an instance of ElectronicDevice with a work_power of 30
    charger = ElectronicDevice(work_power=60)

    # Create an instance of SmartPlug with a rated_power of 90 and an empty list for plugged_devices
    plug = SolarPanel(provided_power=90, powered_devices=[], slots=5)

    obj_list = [hairdryer, fan]

    assert e.enforce(obj_list, plug, "plug_in")
    plug.plug_in(hairdryer)

    # assert e.enforce(fan, plug, "plug_in")
    # plug.plug_in(fan)
    #
    # assert not e.enforce(charger, plug, "plug_in")
