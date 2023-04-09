from dataclasses import dataclass


@dataclass
class Fireplace:
    turned_on: bool

    def get_fire_status(self):
        return self.turned_on

    def get_json_fire_status(self):
        return {"turned_on": self.turned_on}

    def set_fire_status(self, new_value):
        self.turned_on = new_value
