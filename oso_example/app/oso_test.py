from oso import Oso

from electronic_device import ElectronicDevice
from smart_plug import SmartPlug


# Check if the device is allowed to plug into the smart plug
def test_basic_oso():
    # Initialize the Oso object. This object is usually used globally throughout
    # an application.
    oso = Oso()

    # Tell Oso about the data you will authorize. These types can be referenced
    # in the policy.
    oso.register_class(ElectronicDevice)
    oso.register_class(SmartPlug)

    # Load Polar policy file
    oso.load_files(["main.polar"])

    # Create an instance of ElectronicDevice with a work_power of 30
    hairdryer = ElectronicDevice(work_power=30)

    # Create an instance of SmartPlug with a rated_power of 50 and an empty list for plugged_devices
    plug = SmartPlug(rated_power=80, plugged_devices=[], slots=5)

    assert oso.is_allowed(hairdryer, "plug_in", plug)
    plug.plug_in(hairdryer)
    # Check that the device was added to the list of plugged devices on the smart plug
    assert hairdryer in plug.plugged_devices
    assert plug.rated_power == 50
    assert plug.slots == 4

    # Check that a not connected device cannot be plugged out of the smart plug
    plug.plug_out(ElectronicDevice(work_power=50))
    assert plug.rated_power == 50
    assert plug.slots == 4
