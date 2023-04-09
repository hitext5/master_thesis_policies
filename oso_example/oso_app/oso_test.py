from oso import Oso

from electronic_device import ElectronicDevice
from solar_panel import SolarPanel


def test_solar_panel():
    # Initialize the Oso object. This object is usually used globally throughout an application.
    oso = Oso()

    # Tell Oso about the data you will authorize. These types can be referenced in the policy.
    oso.register_class(ElectronicDevice)
    oso.register_class(SolarPanel)

    # Load Polar policy file
    oso.load_files(["oso_policy_solar_panel.polar"])

    hairdryer = ElectronicDevice(work_power=40)
    fan = ElectronicDevice(work_power=30)
    charger = ElectronicDevice(work_power=30)
    solar_panel = SolarPanel(provided_power=100, powered_devices=[fan, charger])

    assert oso.is_allowed(hairdryer, "plug_in", solar_panel)
