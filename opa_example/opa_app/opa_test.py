from datetime import datetime

import requests
import subprocess

from electronic_device import ElectronicDevice
from owner_location import ApartmentOwner
from smoke_detector import SmokeDetector
from solar_panel import SolarPanel
from clock import Clock
from thermometer import Thermometer
from weather_station import WeatherStation
from window_shade import WindowShade


# The server has to be running for the tests to work.
# Run server with opa run --server in the terminal manually before running the tests.

def test_open_door():
    # Start the OPA server
    # Increases the test evaluation time by almost 1 second
    # For better comparison with the other tests, the server should be started manually
    process = subprocess.Popen("opa run --server ")

    # Load the policies into the OPA server
    requests.put("http://localhost:8181/v1/policies/open_door_and_window",
                 data=open("opa_policy_open_door_and_window.rego", "r").read())

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

    # Stop the OPA server
    process.terminate()


def test_solar_panel():
    # Start the OPA server
    process = subprocess.Popen("opa run --server ")

    # Load the policies into the OPA server
    requests.put("http://localhost:8181/v1/policies/solar_panel",
                 data=open("opa_policy_solar_panel.rego", "r").read())

    hairdryer = ElectronicDevice(work_power=40)
    fan = ElectronicDevice(work_power=30)
    charger = ElectronicDevice(work_power=30)
    solar_panel = SolarPanel(provided_power=110, powered_devices=[hairdryer, fan])

    def eval_policy_solar_panel(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/solar_panel",
            json={"input": input_data}
        )
        if response.status_code != 200:
            raise Exception("Error evaluating policy: " + response.text)
        if 'result' not in response.json():
            return False
        return response.json()["result"]

    assert eval_policy_solar_panel({"requesting_device": charger.get_json_work_power(),
                                    "solar_panel": {"provided_power": solar_panel.get_provided_power(),
                                                    "powered_devices": solar_panel.get_powered_devices()}})
    # Stop the OPA server
    process.terminate()


def test_close_door():
    process = subprocess.Popen("opa run --server ")

    requests.put("http://localhost:8181/v1/policies/open_door_and_window",
                 data=open("opa_policy_open_door_and_window.rego", "r").read())

    ron = ApartmentOwner(at_home=False)

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

    assert not eval_policy_open_doors_and_windows({"owner_location": ron.get_json_location()})

    process.terminate()


def test_light_on():
    process = subprocess.Popen("opa run --server ")

    requests.put("http://localhost:8181/v1/policies/open_door_and_window",
                 data=open("opa_policy_open_door_and_window.rego", "r").read())
    requests.put("http://localhost:8181/v1/policies/light_on",
                 data=open("opa_policy_light_on.rego", "r").read())

    echo_dot = Clock(current_time=datetime.now().hour)
    # echo_dot = Clock(current_time=4)
    ron = ApartmentOwner(at_home=False)

    def eval_policy_light_on(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/light_on/allow",
            json={"input": input_data}
        )
        if response.status_code != 200:
            raise Exception("Error evaluating policy: " + response.text)
        if 'result' not in response.json():
            return False
        return response.json()["result"]

    assert eval_policy_light_on({"clock": echo_dot.get_json_current_time(),
                                 "owner_location": ron.get_json_location()})

    process.terminate()


def test_open_window_and_shade():
    process = subprocess.Popen("opa run --server ")

    requests.put("http://localhost:8181/v1/policies/open_door_and_window",
                 data=open("opa_policy_open_door_and_window.rego", "r").read())
    requests.put("http://localhost:8181/v1/policies/window_with_weather",
                 data=open("opa_policy_window_with_weather.rego", "r").read())
    requests.put("http://localhost:8181/v1/policies/shade_with_weather",
                 data=open("opa_policy_shade_with_weather.rego", "r").read())

    ron = ApartmentOwner(at_home=True)
    kitchen_window_shade = WindowShade(closed_state=True)
    ws_2902 = WeatherStation(wind_speed=10, weather_condition="sunny")

    def eval_policy_widow_shade_open(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/shade_with_weather/allow",
            json={"input": input_data}
        )
        if response.status_code != 200:
            raise Exception("Error evaluating policy: " + response.text)
        if 'result' not in response.json():
            return False
        return response.json()["result"]

    def eval_policy_widow_open(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/window_with_weather/allow",
            json={"input": input_data}
        )
        if response.status_code != 200:
            raise Exception("Error evaluating policy: " + response.text)
        if 'result' not in response.json():
            return False
        return response.json()["result"]

    assert eval_policy_widow_shade_open({"owner_location": ron.get_json_location(),
                                         "weather": {"wind_speed": ws_2902.get_wind_speed(),
                                                     "weather_condition": ws_2902.get_weather_condition()}})
    kitchen_window_shade.set_closed_state(False)

    assert eval_policy_widow_open({"owner_location": ron.get_json_location(),
                                   "window_shade": kitchen_window_shade.get_json_closed_state(),
                                   "weather": {"wind_speed": ws_2902.get_wind_speed(),
                                               "weather_condition": ws_2902.get_weather_condition()}})

    process.terminate()


def test_fireplace_and_ac():
    process = subprocess.Popen("opa run --server ")

    requests.put("http://localhost:8181/v1/policies/fireplace_and_ac",
                 data=open("opa_policy_fireplace_and_ac.rego", "r").read())

    indoor_thermometer = Thermometer(temperature=20)
    ron = ApartmentOwner(at_home=False)

    def eval_policy_fireplace_and_ac(input_data):
        response = requests.post(
            "http://localhost:8181/v1/data/fireplace_and_ac/allow",
            json={"input": input_data}
        )
        if response.status_code != 200:
            raise Exception("Error evaluating policy: " + response.text)
        if 'result' not in response.json():
            return False
        return response.json()["result"]

    assert eval_policy_fireplace_and_ac({"owner_location": ron.get_json_location(),
                                         "thermometer": indoor_thermometer.get_json_temperature()})

    process.terminate()
