package shade_with_weather

import data.open_door_and_window

allow {
    open_door_and_window.owner_at_home
    windless
    sunny
}

windless {
    input.weather.wind_speed <= 12
}

sunny {
    input.weather.weather_condition == "sunny"
}