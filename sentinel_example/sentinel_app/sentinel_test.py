import subprocess

from electronic_device import ElectronicDevice
from smart_plug import SmartPlug


def test_basic_sentinel():
    # This function updates the sentinel policy file with the new plug rated power
    def update_sentinel_policy(new_content: str):
        with open("sentinel_policy.sentinel", "r") as file:
            data = file.read()
            start_index = data.index('plug_slots')
            end_index = data.index('enough_power')
            data = data[:start_index] + new_content + data[end_index:]
        with open("sentinel_policy.sentinel", "w") as file:
            file.write(data)

    # Define a function to update the plug_json
    def apply_policy():
        try:
            output = subprocess.check_output("sentinel apply sentinel_policy.sentinel")
            output_str = output.decode("utf-8")
            if "Pass" in output_str:
                return True
            else:
                return False
        except subprocess.CalledProcessError:
            return False
    # Create an instance of ElectronicDevice with a work_power of 40
    hairdryer = ElectronicDevice(work_power=40)

    # Create an instance of ElectronicDevice with a work_power of 30
    fan = ElectronicDevice(work_power=30)

    # Create an instance of ElectronicDevice with a work_power of 30
    charger = ElectronicDevice(work_power=30)

    # Create an instance of SmartPlug with a rated_power of 90 and an empty list for plugged_devices
    plug = SmartPlug(rated_power=90, plugged_devices=[], slots=5)

    # update_sentinel_policy(f'plug_slots = {plug.slots}\nplug_rated_power = {plug.rated_power}\n'
    #                        f'electronic_device_work_power = {hairdryer.work_power}\ninput_act = "plug_in"\n\n')
    apply_policy()
    # plug.plug_in(hairdryer)
    #
    # update_sentinel_policy(f'plug_slots = {plug.slots}\nplug_rated_power = {plug.rated_power}\n'
    #                        f'electronic_device_work_power = {fan.work_power}\ninput_act = "plug_in"\n\n')
    # assert apply_policy()
    # plug.plug_in(fan)
    #
    # update_sentinel_policy(f'plug_slots = {plug.slots}\nplug_rated_power = {plug.rated_power}\n'
    #                        f'electronic_device_work_power = {charger.work_power}\ninput_act = "plug_in"\n\n')
    # assert not apply_policy()
