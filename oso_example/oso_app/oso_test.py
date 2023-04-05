from oso import Oso

from electronic_device import ElectronicDevice
from solar_panel import SolarPanel


# Check if the device is allowed to plug into the smart plug
def test_basic_oso():
    # Initialize the Oso object. This object is usually used globally throughout
    # an application.
    oso = Oso()

    # Tell Oso about the data you will authorize. These types can be referenced
    # in the policy.
    oso.register_class(ElectronicDevice)
    oso.register_class(SolarPanel)

    # Load Polar policy file
    oso.load_files(["oso_policy.polar"])

    # Create an instance of ElectronicDevice with a work_power of 40
    hairdryer = ElectronicDevice(work_power=40)

    # Create an instance of ElectronicDevice with a work_power of 30
    fan = ElectronicDevice(work_power=30)

    # Create an instance of ElectronicDevice with a work_power of 30
    charger = ElectronicDevice(work_power=30)

    # Create an instance of SmartPlug with a rated_power of 90 and an empty list for plugged_devices
    plug = SolarPanel(provided_power=90, powered_devices=[], slots=5)

    assert oso.is_allowed(hairdryer, "plug_in", plug)
    plug.plug_in(hairdryer)

    assert oso.is_allowed(fan, "plug_in", plug)
    plug.plug_in(fan)

    assert not oso.is_allowed(charger, "plug_in", plug)

