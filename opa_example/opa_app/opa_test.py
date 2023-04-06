import requests
import subprocess

from electronic_device import ElectronicDevice
from owner_location import ApartmentOwner
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
    requests.put("http://localhost:8181/v1/policies/smoke_detector",
                 data=open("opa_policy_smoke_detected.rego", "r").read())
    requests.put("http://localhost:8181/v1/policies/solar_panel",
                 data=open("opa_policy_solar_panel.rego", "r").read())
    requests.put("http://localhost:8181/v1/policies/close_doors_and_windows",
                 data=open("opa_policy_close_door_window.rego", "r").read())

    # Open the door policy
    living_room_smoke_detector = SmokeDetector(smoke_detected=True)

    # Define a function to evaluate the policy for the open door with input data
    def eval_policy_smoke_detector(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/smoke_detector/smoke_detected",
            json={"input": input_data}
        )
        return response.json()["result"]

    # Assert that the policy returns True
    assert eval_policy_smoke_detector({"smoke_detector": living_room_smoke_detector.get_json_smoke_detected()})

    # Solar panel policy
    hairdryer = ElectronicDevice(work_power=40)
    fan = ElectronicDevice(work_power=30)
    charger = ElectronicDevice(work_power=30)
    solar_panel = SolarPanel(provided_power=110, powered_devices=[hairdryer, fan])

    # Define a function to evaluate the policy for the solar panel with input data
    def eval_policy_solar_panel(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/solar_panel/enough_power",
            json={"input": input_data}
        )
        return response.json()["result"]

    # Assert that the policy returns True
    assert eval_policy_solar_panel({"requesting_device": charger.get_json_work_power(),
                                    "solar_panel": {"provided_power": solar_panel.get_rated_power(),
                                                    "powered_devices": solar_panel.get_powered_devices()}})

    ron = ApartmentOwner(at_home=False)

    # Define a function to evaluate the policy for the owner location with input data
    def eval_policy_close_doors_and_windows(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/close_doors_and_windows/owner_absent",
            json={"input": input_data}
        )
        return response.json()["result"]

    # Assert that the policy returns True
    assert eval_policy_close_doors_and_windows({"owner_location": ron.get_json_location()})

    # Stop the OPA server
    process.terminate()
