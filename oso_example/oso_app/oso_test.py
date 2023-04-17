from datetime import datetime

from oso import Oso

from clock import Clock
from door import Door
from electronic_device import ElectronicDevice
from light_and_door import LightAndDoor
from light_bulb import LightBulb
from location_and_time import LocationAndTime
from owner_location import ApartmentOwner
from smoke_detector import SmokeDetector
from solar_panel import SolarPanel


def test_open_door():
    # Initialize the Oso object. This object is usually used globally throughout an application.
    oso = Oso()

    # Tell Oso about the data you will authorize. These types can be referenced in the policy.
    oso.register_class(SmokeDetector)
    oso.register_class(Door)
    oso.register_class(ApartmentOwner)

    # Load Polar policy file
    oso.load_files(["oso_policy_open_door_and_window.polar"])

    smoke_detector = SmokeDetector(smoke_detected=True)
    door = Door(locked=True)

    assert oso.is_allowed(smoke_detector, "unlock", door)


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

    assert oso.is_allowed(hairdryer, "power", solar_panel)


def test_close_door():
    # Initialize the Oso object. This object is usually used globally throughout an application.
    oso = Oso()

    # Tell Oso about the data you will authorize. These types can be referenced in the policy.
    oso.register_class(SmokeDetector)
    oso.register_class(Door)
    oso.register_class(ApartmentOwner)

    # Load Polar policy file
    oso.load_files(["oso_policy_open_door_and_window.polar"])

    ron = ApartmentOwner(at_home=False)
    door = Door(locked=False)

    assert oso.is_allowed(ron, "lock", door)


def test_light_on():
    # Initialize the Oso object. This object is usually used globally throughout an application.
    oso = Oso()

    # Tell Oso about the data you will authorize. These types can be referenced in the policy.
    oso.register_class(SmokeDetector)
    oso.register_class(Door)
    oso.register_class(ApartmentOwner)
    oso.register_class(Clock)
    oso.register_class(LocationAndTime)
    oso.register_class(LightBulb)
    oso.register_class(LightAndDoor)

    # Load Polar policy files
    oso.load_files(["oso_policy_light_on.polar", "oso_policy_open_door_and_window.polar"])

    echo_dot = Clock(current_time=datetime.now().hour)
    # echo_dot = Clock(current_time=4)
    ron = ApartmentOwner(at_home=False)
    location_and_time = LocationAndTime(ron, echo_dot)
    light_bulb = LightBulb(turned_on=False)
    door = Door(locked=False)
    light_and_door = LightAndDoor(door, light_bulb)

    assert oso.is_allowed(location_and_time, "turn_on", light_and_door)
