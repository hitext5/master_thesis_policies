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
    requests.put("http://localhost:8181/v1/policies/solar_panel",
                 data=open("opa_policy_solar_panel.rego", "r").read())
    requests.put("http://localhost:8181/v1/policies/open_door_and_window",
                 data=open("opa_policy_open_door_and_window.rego", "r").read())

    # Open the door policy
    living_room_smoke_detector = SmokeDetector(smoke_detected=True)

    def eval_policy_open_doors_and_windows(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/open_door_and_window/allow",
            json={"input": input_data}
        )
        if response.status_code != 200:
            raise Exception("Error evaluating policy: " + response.text)
        if 'result' not in response.json():
            return False
        return response.json()["result"]

    assert eval_policy_open_doors_and_windows({"smoke_detector": living_room_smoke_detector.get_json_smoke_detected()})

    # Solar panel policy
    hairdryer = ElectronicDevice(work_power=40)
    fan = ElectronicDevice(work_power=30)
    charger = ElectronicDevice(work_power=30)
    solar_panel = SolarPanel(provided_power=110, powered_devices=[hairdryer, fan])

    def eval_policy_solar_panel(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/solar_panel/enough_power",
            json={"input": input_data}
        )
        if response.status_code != 200:
            raise Exception("Error evaluating policy: " + response.text)
        if 'result' not in response.json():
            return False
        return response.json()["result"]

    assert eval_policy_solar_panel({"requesting_device": charger.get_json_work_power(),
                                    "solar_panel": {"provided_power": solar_panel.get_rated_power(),
                                                    "powered_devices": solar_panel.get_powered_devices()}})

    # Close the door policy
    ron = ApartmentOwner(at_home=False)

    assert not eval_policy_open_doors_and_windows({"owner_location": ron.get_json_location()})

    # Stop the OPA server
    process.terminate()
