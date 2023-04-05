import requests

from electronic_device import ElectronicDevice
from solar_panel import SolarPanel

plug_json = {}  # Define plug_json in the global scope


# The server has to be running for the tests to work.
# Run server with opa run --server opa_policy_solar_panel.rego

# Check if the device is allowed to plug into the smart plug
def test_basic_opa():
    # Define a function to evaluate the policy with input data
    def eval_policy(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/opa_policy/allow",
            json={"input": input_data}
        )
        return response.json()["result"]

    # Create an instance of ElectronicDevice with a work_power of 40
    hairdryer = ElectronicDevice(work_power=40)

    # Create an instance of ElectronicDevice with a work_power of 30
    fan = ElectronicDevice(work_power=30)

    # Create an instance of ElectronicDevice with a work_power of 30
    charger = ElectronicDevice(work_power=30)

    # Create an instance of SmartPlug with a rated_power of 90 and an empty list for plugged_devices
    solar_panel = SolarPanel(provided_power=110, powered_devices=[])

    assert eval_policy({"requesting_device": charger.get_json_work_power(),
                        "solar_panel": {"provided_power": solar_panel.get_rated_power(),
                                        "powered_devices": solar_panel.get_powered_devices()}})
