import requests
import subprocess

from electronic_device import ElectronicDevice
from smoke_detector import SmokeDetector
from solar_panel import SolarPanel


# The server has to be running for the tests to work.
# Run server with opa run --server in the terminal manually before running the tests.

def test_basic_opa():
    # Start the OPA server
    # Increases the test evaluation time by almost 1 second
    # For better comparison with the other tests, the server should be started manually
    process = subprocess.Popen("opa run --server ")

    # Load the policies into the OPA server
    requests.put("http://localhost:8181/v1/policies/open_door",
                 data=open("opa_policy_open_door.rego", "r").read())
    requests.put("http://localhost:8181/v1/policies/solar_panel",
                 data=open("opa_policy_solar_panel.rego", "r").read())

    # Create an instance of SmokeDetector with a smoke_detected attribute of True
    living_room_smoke_detector = SmokeDetector(smoke_detected=True)

    # Define a function to evaluate the policy for the open door with input data
    def eval_policy_open_door(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/open_door/smoke_detected",
            json={"input": input_data}
        )
        return response.json()["result"]

    # Assert that the policy returns True
    assert eval_policy_open_door({"smoke_detector": living_room_smoke_detector.get_json_smoke_detected()})

    # Define a function to evaluate the policy for the solar panel with input data
    def eval_policy_solar_panel(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/solar_panel/enough_power",
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
    solar_panel = SolarPanel(provided_power=110, powered_devices=[hairdryer, fan])

    # Assert that the policy returns True
    assert eval_policy_solar_panel({"requesting_device": charger.get_json_work_power(),
                                    "solar_panel": {"provided_power": solar_panel.get_rated_power(),
                                                    "powered_devices": solar_panel.get_powered_devices()}})
    # Stop the OPA server
    process.terminate()
