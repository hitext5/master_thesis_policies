package opa_policy

default allow = false

allow {
    enough_power(input.requesting_device, input.solar_panel)
}

enough_power(requesting_device, solar_panel) {
    total_power := sum([device.work_power | device := solar_panel.powered_devices[_]]) + requesting_device.work_power
    solar_panel.provided_power >= total_power
}

# The above policy is a simple example of how to use OPA to enforce a policy.
# The policy is a simple rule that checks if the total power of all the devices powered by the solar panel
# is less than the power provided by the solar panel. If the total power is less than the power provided
# by the solar panel, then the policy allows the request. The policy is enforced by the OPA server, which is a REST API
# that can be queried with a JSON payload. The JSON payload is the input to the policy. The policy is evaluated and the
# result is returned in the response.