from dataclasses import dataclass


@dataclass
class WeatherStation:
    wind_speed: float
    weather_condition: str

    def get_wind_speed(self):
        return self.wind_speed

    def get_weather_condition(self):
        return self.weather_condition

