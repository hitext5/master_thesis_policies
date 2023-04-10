from electronic_device import ElectronicDevice
from python_example import python_policy_solar_panel as pp
from solar_panel import SolarPanel

hairdryer = ElectronicDevice(work_power=40)
fan = ElectronicDevice(work_power=30)
charger = ElectronicDevice(work_power=30)
solar_panel = SolarPanel(provided_power=110, powered_devices=[hairdryer, fan])

# When the washing machine is turned on a request is sent to the solar panel to see if it has enough power to
# power the washing machine. If it does not have enough power, the washing machine will not run.
if pp.eval_policy_solar_panel(charger, solar_panel):
    print("The solar panel has enough power to power the washing machine.")
else:
    print("The solar panel does not have enough power to power the washing machine.")
