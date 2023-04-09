package fireplace_and_ac

import data.open_door_and_window

allow {
    not open_door_and_window.owner_at_home
    high_temperature
}

high_temperature {
    input.thermometer.temperature > 15
}