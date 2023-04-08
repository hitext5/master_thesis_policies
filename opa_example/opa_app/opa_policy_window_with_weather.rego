package window_with_weather

import data.open_door_and_window
import data.shade_with_weather

allow {
    open_door_and_window.owner_at_home
    shade_with_weather.windless
    shade_with_weather.sunny
    shade_open
}

shade_open {
    not input.window_shade.closed_state
}
