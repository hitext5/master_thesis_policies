from dataclasses import dataclass


@dataclass
class Thermometer:
    temperature: float

    def get_temperature(self):
        return self.temperature

    def get_json_temperature(self):
        return {"temperature": self.temperature}
