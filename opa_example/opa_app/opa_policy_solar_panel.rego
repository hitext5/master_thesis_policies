package solar_panel

enough_power {
    total_power := sum([device.work_power | device := input.solar_panel.powered_devices[_]]) + input.requesting_device.work_power
    input.solar_panel.provided_power >= total_power
}
