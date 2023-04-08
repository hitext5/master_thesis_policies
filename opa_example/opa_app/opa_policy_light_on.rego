package light_on

# Reuse the method to check if the owner is at home
import data.open_door_and_window

allow {
    after_sunset or before_sunrise
    not open_door_and_window.owner_at_home
}

after_sunset {
    input.clock.current_time > 18
}

before_sunrise {
    input.clock.current_time < 6
}

# The light should be on if it is after sunset or before sunrise and the owner is not at home

