package opa_policy

default allow = false

allow {
    input.act == "plug_in"
    enough_power(input.electronic_device, input.smart_plug)
    enough_slots(input.smart_plug)
}

enough_power(electronic_device, smart_plug) {
    count(electronic_device) > 1
    total_power := sum([device.work_power | device := electronic_device[_]])
    smart_plug.rated_power >= total_power
}

enough_power(electronic_device, smart_plug) {
    count(electronic_device) == 1
    smart_plug.rated_power >= electronic_device.work_power
}

enough_slots(smart_plug) {
    smart_plug.slots >= 1
}