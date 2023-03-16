import casbin

from classes import ElectronicDevice, SmartPlug


# Initialize the Casbin object.
e = casbin.Enforcer("model.conf", "policy.csv")

# Create an instance of ElectronicDevice with a work_power of 40
hairdryer = ElectronicDevice(work_power=40)

# Create an instance of ElectronicDevice with a work_power of 30
fan = ElectronicDevice(work_power=30)

# Create an instance of ElectronicDevice with a work_power of 30
charger = ElectronicDevice(work_power=30)

# Create an instance of SmartPlug with a rated_power of 90 and an empty list for plugged_devices
plug = SmartPlug(rated_power=90, plugged_devices=[], slots=5)


# Check if the device is allowed to plug into the smart plug
if e.enforce(fan, plug, "plug_in"):
    plug.plug_in(hairdryer)
    print("Access Granted")
else:
    print("Access Denied")

if e.enforce(fan, plug, "plug_in"):
    plug.plug_in(fan)
    print("Access Granted")
else:
    print("Access Denied")

if e.enforce(charger, plug, "plug_in"):
    plug.plug_in(charger)
    print("Access Granted")
else:
    print(f"Access Denied: The smart plug has {plug.rated_power} energy left but the device needs {charger.work_power} "
          f"energy to work.")
