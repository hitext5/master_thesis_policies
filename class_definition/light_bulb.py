from dataclasses import dataclass


@dataclass
class LightBulb:
    turned_on: bool

    def get_light_status(self):
        return self.turned_on

    def get_json_light_status(self):
        return {"turned_on": self.turned_on}

    def set_light_status(self, new_value):
        self.turned_on = new_value
