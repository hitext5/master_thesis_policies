import requests

from electronic_device import ElectronicDevice
from smart_plug import SmartPlug

plug_json = {}  # Define plug_json in the global scope


# The server has to be running for the tests to work.
# Run server with opa run --server opa_policy.rego

# Check if the device is allowed to plug into the smart plug
def test_basic_casbin():
    # Define a function to evaluate the policy with input data
    def eval_policy(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/opa_policy/allow",
            json={"input": input_data}
        )
        return response.json()["result"]

    # Define a function to update the plug_json
    def update_plug_json():
        global plug_json
        plug_json = {"rated_power": plug.rated_power, "slots": plug.slots}

    # Create an instance of ElectronicDevice with a work_power of 40
    hairdryer = ElectronicDevice(work_power=40)
    hairdryer_json = {"work_power": hairdryer.work_power}

    # Create an instance of ElectronicDevice with a work_power of 30
    fan = ElectronicDevice(work_power=30)
    fan_json = {"work_power": fan.work_power}

    # Create an instance of ElectronicDevice with a work_power of 30
    charger = ElectronicDevice(work_power=30)
    charger_json = {"work_power": charger.work_power}

    # Create an instance of SmartPlug with a rated_power of 90 and an empty list for plugged_devices
    plug = SmartPlug(rated_power=90, plugged_devices=[], slots=5)
    update_plug_json()

    assert eval_policy({"electronic_device": hairdryer_json, "smart_plug": plug_json, "act": "plug_in"})
    plug.plug_in(hairdryer)
    update_plug_json()

    assert eval_policy({"electronic_device": fan_json, "smart_plug": plug_json, "act": "plug_in"})
    plug.plug_in(fan)
    update_plug_json()

    assert not eval_policy({"electronic_device": charger_json, "smart_plug": plug_json, "act": "plug_in"})
